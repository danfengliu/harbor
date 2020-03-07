# -*- coding: utf-8 -*-

import os
import base
import json

def load_bundle(service_image, invocation_image):
    bundle_file = "./tests/apitests/python/bundle_data/bundle.json"
    bundle_tmpl_file = "./tests/apitests/python/bundle_data/bundle.json.tmpl"
    with open(bundle_tmpl_file,'r') as load_f:
        load_dict = json.load(load_f)
        print "load_dict:", load_dict
        print "load_dict-invocationImages:", load_dict["invocationImages"][0]["contentDigest"]
        #load_dict["images"]["hello"]["image"] = service_image
        #load_dict["invocationImages"][0]["image"] = invocation_image
        bundle_str = json.dumps(load_dict)
        print "bundle_str:", bundle_str
        with open(bundle_file,'w') as dump_f:
            dump_f.write(bundle_str)
            dump_f.close()
        return bundle_file

def cnab_fixup_bundle(bundle_file, target, auto_update_bundle = True):
    fixed_bundle_file = "./tests/apitests/python/bundle_data/fixed-bundle.json"
    command = ["cnab-to-oci", "--log-level", "error", "fixup", bundle_file, "--target", target, "--bundle", fixed_bundle_file]
    if auto_update_bundle == True:
         command.append("--auto-update-bundle")
         #fixed_bundle_file = bundle_file
    print "Command: ", command
    ret = base.run_command(command)
    print "Command return: ", ret
    return fixed_bundle_file

def cnab_push_bundle(bundle_file, target):
    command = ["cnab-to-oci", "push", bundle_file, "--target", target, "--auto-update-bundle"]
    print "Command: ", command
    ret = base.run_command(command)
    print "Command return: ", ret

def push_cnab_bundle(service_image, invocation_image, target, auto_update_bundle = True):
    bundle_file = load_bundle(service_image, invocation_image)
    fixed_bundle_file = cnab_fixup_bundle(bundle_file, target, auto_update_bundle = auto_update_bundle)
    cnab_push_bundle(fixed_bundle_file, target)
