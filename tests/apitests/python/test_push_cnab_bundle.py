from __future__ import absolute_import


import unittest

import library.repository
import library.cnab
from testutils import ADMIN_CLIENT
from testutils import harbor_server

from testutils import TEARDOWN
from library.project import Project
from library.user import User
from library.repository import Repository
from library.artifact import Artifact
from library.repository import push_special_image_to_project
from library.docker_api import DockerAPI

class TestProjects(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.project= Project()
        self.user= User()
        self.artifact = Artifact(api_type='artifact')
        self.repo= Repository(api_type='repository')
        self.url = ADMIN_CLIENT["endpoint"]
        self.user_push_chart_password = "Aa123456"

    @classmethod
    def tearDownClass(self):
        print "Case completed"

    @unittest.skipIf(TEARDOWN == True, "Test data won't be erased.")
    def test_ClearData(self):
        #1. Delete repository chart(CA) by user(UA);
        self.repo.delete_repoitory(TestProjects.project_push_chart_name, self.repo_name, **TestProjects.USER_CLIENT)

        #2. Delete project(PA);
        self.project.delete_project(TestProjects.project_push_chart_id, **TestProjects.USER_CLIENT)

        #3. Delete user(UA).
        self.user.delete_user(TestProjects.user_id, **ADMIN_CLIENT)

    def testPushChartByHelmChartCLI(self):
        """
        Test case:
            Push Chart File By Helm Chart CLI
        Test step and expected result:
            1. Create a new user(UA);
            2. Create a new project(PA) by user(UA);
            3. Push an chart(CA) to Harbor by helm3 registry/chart CLI successfully;
            4. Get chart(CA) from Harbor successfully;
            5. TO_DO: Verify this chart artifact information, like digest.
        Tear down:
            1. Delete repository chart(CA) by user(UA);
            2. Delete project(PA);
            3. Delete user(UA).
        """
        #1. Create a new user(UA);
        TestProjects.user_id, user_name = self.user.create_user(user_password = self.user_push_chart_password, **ADMIN_CLIENT)
        TestProjects.USER_CLIENT=dict(endpoint = self.url, username = user_name, password = self.user_push_chart_password)

        #2. Create a new project(PA) by user(UA);
        TestProjects.project_push_chart_id, TestProjects.project_push_chart_name = self.project.create_project(metadata = {"public": "false"}, **TestProjects.USER_CLIENT)

        _docker_api = DockerAPI()
        _docker_api.docker_image_pull("hello-world", tag = "latest")
        _docker_api.docker_image_pull("busybox", tag = "latest")

        #repo, image_id = push_special_image_to_project(TestProjects.project_push_chart_name, harbor_server, user_name, self.user_push_chart_password, "test1", ['1.0'])
        cnab_repo_name = "test_cnab"
        target = harbor_server + "/" + TestProjects.project_push_chart_name  + "/" + cnab_repo_name
        library.cnab.push_cnab_bundle("hello-world:latest", "busybox:latest", target)

        #5. Get index(IA) from Harbor successfully;
        index_data = self.repo.get_repository(TestProjects.project_push_chart_name, cnab_repo_name, **TestProjects.USER_CLIENT)
        print "index_data:", index_data

if __name__ == '__main__':
    unittest.main()

