# from __future__ import absolute_import, division, print_function, unicode_literals
#
# import base64
# import warnings
# from builtins import open, bytes, str
#
# import asn1
# import binascii
#
#
# def read_pem(input_file):
#     """Read PEM formatted input."""
#     data = []
#     state = 0
#     for line in input_file:
#         if state == 0:
#             if line.startswith('-----BEGIN'):
#                 state = 1
#         elif state == 1:
#             if line.startswith('-----END'):
#                 state = 2
#             else:
#                 data.append(line)
#         elif state == 2:
#             break
#     if state != 2:
#         raise ValueError('No PEM encoded input found')
#     data = ''.join(data)
#     return base64.b64decode(data)
#
#
# tag_id_to_string_map = {
#     asn1.Numbers.Boolean: "BOOLEAN",
#     asn1.Numbers.Integer: "INTEGER",
#     asn1.Numbers.BitString: "BIT STRING",
#     asn1.Numbers.OctetString: "OCTET STRING",
#     asn1.Numbers.Null: "NULL",
#     asn1.Numbers.ObjectIdentifier: "OBJECT",
#     asn1.Numbers.PrintableString: "PRINTABLESTRING",
#     asn1.Numbers.IA5String: "IA5STRING",
#     asn1.Numbers.UTCTime: "UTCTIME",
#     asn1.Numbers.GeneralizedTime: "GENERALIZED TIME",
#     asn1.Numbers.Enumerated: "ENUMERATED",
#     asn1.Numbers.Sequence: "SEQUENCE",
#     asn1.Numbers.Set: "SET"
# }
#
# # 4种类型
# class_id_to_string_map = {
#     asn1.Classes.Universal: "Universal",  # 用来表示在所有应用中都具有相同意义的类型. 这些类型定义在 X.208
#     asn1.Classes.Application: "Application",  # 用来表示针对于具体应用的类型. 在不同的应用中这些类型的意义往往不同
#     asn1.Classes.Context: "Context",  # 用来表示针对于具体上下文该类型意义会变化的类型
#     asn1.Classes.Private: "Private"  # 用来表示针对用于具体企业的类型
# }
#
# object_id_to_string_map = {
#     "1.2.840.113549.1.1.1": "rsaEncryption",
#     "1.2.840.113549.1.1.5": "sha1WithRSAEncryption",
#
#     "1.3.6.1.5.5.7.1.1": "authorityInfoAccess",
#
#     "2.5.4.3": "commonName",
#     "2.5.4.4": "surname",
#     "2.5.4.5": "serialNumber",
#     "2.5.4.6": "countryName",
#     "2.5.4.7": "localityName",
#     "2.5.4.8": "stateOrProvinceName",
#     "2.5.4.9": "streetAddress",
#     "2.5.4.10": "organizationName",
#     "2.5.4.11": "organizationalUnitName",
#     "2.5.4.12": "title",
#     "2.5.4.13": "description",
#     "2.5.4.42": "givenName",
#
#     "1.2.840.113549.1.9.1": "emailAddress",
#
#     "2.5.29.14": "X509v3 Subject Key Identifier",
#     "2.5.29.15": "X509v3 Key Usage",
#     "2.5.29.16": "X509v3 Private Key Usage Period",
#     "2.5.29.17": "X509v3 Subject Alternative Name",
#     "2.5.29.18": "X509v3 Issuer Alternative Name",
#     "2.5.29.19": "X509v3 Basic Constraints",
#     "2.5.29.30": "X509v3 Name Constraints",
#     "2.5.29.31": "X509v3 CRL Distribution Points",
#     "2.5.29.32": "X509v3 Certificate Policies Extension",
#     "2.5.29.33": "X509v3 Policy Mappings",
#     "2.5.29.35": "X509v3 Authority Key Identifier",
#     "2.5.29.36": "X509v3 Policy Constraints",
#     "2.5.29.37": "X509v3 Extended Key Usage",
#
#     "1.2.840.10045.2.1": "ecPublicKey",
#     # "Elliptic curve public key cryptography"  # See IETF RFC 3279, RFC 5480 and RFC 5753.
#     "1.2.156.10197.1.301": "SM2",
#     "1.2.156.10197.1.501": "SM3WithSM2",
#     "1.2.156.10197.1.502": "sha1withSM2",
#     "1.2.156.10197.1.503": "sha256withSM2",
#     "1.2.156.10197.1.504": "sm3withRSAEncryption",
#
# }
#
#
# def tag_id_to_string(identifier):
#     """Return a string representation of a ASN.1 id."""
#     if identifier in tag_id_to_string_map:
#         return tag_id_to_string_map[identifier]
#     return '{:#02x}'.format(identifier)
#
#
# def class_id_to_string(identifier):
#     """Return a string representation of an ASN.1 class."""
#     if identifier in class_id_to_string_map:
#         return class_id_to_string_map[identifier]
#     raise ValueError('Illegal class: {:#02x}'.format(identifier))
#
#
# def object_identifier_to_string(identifier):
#     if identifier in object_id_to_string_map:
#         return object_id_to_string_map[identifier]
#     return identifier
#
#
# def value_to_string(tag_number, value):
#     if tag_number == asn1.Numbers.ObjectIdentifier:
#         return object_identifier_to_string(value)
#     elif isinstance(value, bytes):
#         return '0x' + str(binascii.hexlify(value).upper())
#     elif isinstance(value, str):
#         return value
#     else:
#         return repr(value)
#
#
# def asn1_load(data: bytes):
#     """load ASN.1 data."""
#     warnings.warn('todo remove by using pyasn1', DeprecationWarning)
#     decoder = asn1.Decoder()
#     decoder.start(data)
#
#     def _load(decoder):
#         result = []
#         while not decoder.eof():
#             tag = decoder.peek()
#             if tag.typ == asn1.Types.Primitive:
#                 tag, value = decoder.read()
#                 result.append({'class': class_id_to_string(tag.cls), 'tag': tag_id_to_string(tag.nr),
#                                'value': value_to_string(tag.nr, value)})
#             elif tag.typ == asn1.Types.Constructed:
#                 decoder.enter()
#                 result.append(_load(decoder))
#                 decoder.leave()
#         return result
#
#     return _load(decoder)
#
