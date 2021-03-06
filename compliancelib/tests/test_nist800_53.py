from unittest import TestCase

import compliancelib
# import sys
import os
import json
import yaml

# sys.path.append(os.path.join('lib'))
# sys.path.append(os.path.join('data'))
from compliancelib import NIST800_53

class NIST800_53Test(TestCase):
    
    def test(self):
        self.assertTrue(True)

    def test_control_list(self):
        self.assertEqual(len(list(NIST800_53.get_control_ids())), 256)

    def test_control_enhancement_list(self):
        self.assertEqual(len(list(NIST800_53.get_control_enhancement_ids())), 666)

    def test_id(self):
        id = "AT-3"
        c = NIST800_53(id)
        self.assertTrue(id == c.id)

    def test_details(self):
        id = "AT-3"
        c = NIST800_53(id)
        self.assertTrue(c.title == "ROLE-BASED SECURITY TRAINING")

    def test_details_control_enhancement(self):
        id = "AU-3 (1)"
        c = NIST800_53(id)
        self.assertTrue(c.title == "ADDITIONAL AUDIT INFORMATION")
        self.assertTrue(c.description == "The information system generates audit records containing the following additional information: [Assignment: organization-defined additional, more detailed information].")

    def test_no_existing_control(self):
        id = "XY-3000"
        c = NIST800_53(id)
        self.assertTrue(c.title == None)
        self.assertTrue(c.description == None)
        self.assertTrue(c.supplemental_guidance == None)
        self.assertTrue(c.responsible == None)
        self.assertTrue(c.details == {})

    def test_details_nonexistent_control(self):
        id = "AX-3"
        c = NIST800_53(id)
        self.assertTrue(c.title == None)

    def test_nonexistent_control_enhancements(self):
        id = "AC-1"
        c = NIST800_53(id)
        self.assertTrue(c.control_enhancements == None)

    def test_supplemental_guidance(self):
        id = "AC-16"
        c = NIST800_53(id)
        self.assertTrue(c.supplemental_guidance == "Information is represented internally within information systems using abstractions known as data structures. Internal data structures can represent different types of entities, both active and passive. Active entities, also known as subjects, are typically associated with individuals, devices, or processes acting on behalf of individuals. Passive entities, also known as objects, are typically associated with data structures such as records, buffers, tables, files, inter-process pipes, and communications ports. Security attributes, a form of metadata, are abstractions representing the basic properties or characteristics of active and passive entities with respect to safeguarding information. These attributes may be associated with active entities (i.e., subjects) that have the potential to send or receive information, to cause information to flow among objects, or to change the information system state. These attributes may also be associated with passive entities (i.e., objects) that contain or receive information. The association of security attributes to subjects and objects is referred to as binding and is typically inclusive of setting the attribute value and the attribute type. Security attributes when bound to data/information, enables the enforcement of information security policies for access control and information flow control, either through organizational processes or information system functions or mechanisms. The content or assigned values of security attributes can directly affect the ability of individuals to access organizational information.\nOrganizations can define the types of attributes needed for selected information systems to support missions/business functions. There is potentially a wide range of values that can be assigned to any given security attribute. Release markings could include, for example, US only, NATO, or NOFORN (not releasable to foreign nationals). By specifying permitted attribute ranges and values, organizations can ensure that the security attribute values are meaningful and relevant. The term security labeling refers to the association of security attributes with subjects and objects represented by internal data structures within organizational information systems, to enable information system-based enforcement of information security policies. Security labels include, for example, access authorizations, data life cycle protection (i.e., encryption and data expiration), nationality, affiliation as contractor, and classification of information in accordance with legal and compliance requirements. The term security marking refers to the association of security attributes with objects in a human-readable form, to enable organizational process-based enforcement of information security policies. The AC-16 base control represents the requirement for user-based attribute association (marking). The enhancements to AC-16 represent additional requirements including information system-based attribute association (labeling). Types of attributes include, for example, classification level for objects and clearance (access authorization) level for subjects. An example of a value for both of these attribute types is Top Secret.")  

    def test_responsible(self):
        # test "organization"
        id = "AT-3"
        c = NIST800_53(id)
        self.assertTrue(c.responsible == "organization")

        id = "AU-8"
        c = NIST800_53(id)
        self.assertTrue(c.responsible == "information system")

        # test "[Withdrawn]"
        id = "SA-7"
        c = NIST800_53("SA-7")
        self.assertTrue(c.responsible == "withdrawn")

    def test_generate_json(self):
        id = "AT-3"
        c = NIST800_53(id)
        j = json.loads(c.format('json'))
        self.assertTrue(j["id"] == c.id)
        self.assertTrue(j["title"] == c.title)
        self.assertTrue(j["description"] == c.description)
        self.assertTrue(j["description_intro"] == c.description_intro)
        self.assertTrue(j["responsible"] == c.responsible)
        self.assertTrue(j["supplemental_guidance"] == c.supplemental_guidance)
        # test for other (not organization, information system, or [Withdrawn])

    def test_generate_yaml(self):
        id = "AT-3"
        c = NIST800_53(id)
        self.assertTrue(c.format('yaml')) == "description: 'The organization provides role-based security training to personnel\n    with assigned security roles and responsibilities:\n\n    a. Before authorizing access to the information system or performing assigned\n    duties;\n\n    b. When required by information system changes; and\n\n    c. [Assignment: organization-defined frequency] thereafter.'\ndescription_intro: 'The organization provides role-based security training to personnel\n    with assigned security roles and responsibilities:'\ndescription_sections:\n- a. Before authorizing access to the information system or performing assigned duties;\n- b. When required by information system changes; and\n- 'c. [Assignment: organization-defined frequency] thereafter.'\nid: AT-3\nresponsible: organization\nsupplemental_guidance: Organizations determine the appropriate content of security\n    training based on the assigned roles and responsibilities of individuals and the\n    specific security requirements of organizations and the information systems to\n    which personnel have authorized access. In addition, organizations provide enterprise\n    architects, information system developers, software developers, acquisition/procurement\n    officials, information system managers, system/network administrators, personnel\n    conducting configuration management and auditing activities, personnel performing\n    independent verification and validation activities, security control assessors,\n    and other personnel having access to system-level software, adequate security-related\n    technical training specifically tailored for their assigned duties. Comprehensive\n    role-based training addresses management, operational, and technical roles and\n    responsibilities covering physical, personnel, and technical safeguards and countermeasures.\n    Such training can include for example, policies, procedures, tools, and artifacts\n    for the organizational security roles defined. Organizations also provide the\n    training necessary for individuals to carry out their responsibilities related\n    to operations and supply chain security within the context of organizational information\n    security programs. Role-based security training also applies to contractors providing\n    services to federal agencies.\ntitle: ROLE-BASED SECURITY TRAINING\n"
        # test for other (not organization, information system, or [Withdrawn])

    def test_generate_control_masonry(self):
        id =  "AT-3"
        c = NIST800_53(id)
        self.assertTrue(c.format('control-masonry') == 'description: The organization provides role-based security training to personnel with\n    assigned security roles and responsibilities&colon; a. Before authorizing access\n    to the information system or performing assigned duties; b. When required by information\n    system changes; and c. [Assignment&colon; organization-defined frequency] thereafter.\ndescription_intro: The organization provides role-based security training to personnel\n    with assigned security roles and responsibilities&colon;\ndescription_sections:\n- a. Before authorizing access to the information system or performing assigned duties;\n- b. When required by information system changes; and\n- c. [Assignment&colon; organization-defined frequency] thereafter.\nid: AT-3\nname: ROLE-BASED SECURITY TRAINING\n')
        # test for other (not organization, information system, or [Withdrawn])


if __name__ == "__main__":
    unittest.main()
