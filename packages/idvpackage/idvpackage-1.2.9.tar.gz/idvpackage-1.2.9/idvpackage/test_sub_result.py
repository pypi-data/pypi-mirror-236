import json

document_report = """{
   "breakdown":{
      "age_validation":{
         "breakdown":{
            "minimum_accepted_age":{
               "properties":{
                  
               },
               "result":"clear"
            }
         },
         "result":"clear"
      },
      "compromised_document":{
         "breakdown":{
            "document_database":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "repeat_attempts":{
               "properties":{
                  
               },
               "result":"clear"
            }
         },
         "result":"clear"
      },
      "data_comparison":{
         "breakdown":{
            "date_of_birth":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "date_of_expiry":{
               "properties":{
                  
               },
               "result":null
            },
            "document_numbers":{
               "properties":{
                  
               },
               "result":null
            },
            "document_type":{
               "properties":{
                  
               },
               "result":null
            },
            "first_name":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "gender":{
               "properties":{
                  
               },
               "result":null
            },
            "issuing_country":{
               "properties":{
                  
               },
               "result":null
            },
            "last_name":{
               "properties":{
                  
               },
               "result":"clear"
            }
         },
         "result":"clear"
      },
      "data_consistency":{
         "breakdown":{
            "date_of_birth":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "date_of_expiry":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "document_numbers":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "document_type":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "first_name":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "gender":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "issuing_country":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "last_name":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "multiple_data_sources_present":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "nationality":{
               "properties":{
                  
               },
               "result":"clear"
            }
         },
         "result":"clear"
      },
      "data_validation":{
         "breakdown":{
            "barcode":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "date_of_birth":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "document_expiration":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "document_numbers":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "expiry_date":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "gender":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "mrz":{
               "properties":{
                  
               },
               "result":"clear"
            }
         },
         "result":"clear"
      },
      "image_integrity":{
         "breakdown":{
            "colour_picture":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "conclusive_document_quality":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "image_quality":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "supported_document":{
               "properties":{
                  
               },
               "result":"clear"
            }
         },
         "result":"clear"
      },
      "issuing_authority":{
         "breakdown":{
            "nfc_active_authentication":{
               "properties":{
                  
               },
               "result":null
            },
            "nfc_passive_authentication":{
               "properties":{
                  
               },
               "result":null
            }
         },
         "result":null
      },
      "police_record":{
         "result":"clear"
      },
      "visual_authenticity":{
         "breakdown":{
            "digital_tampering":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "face_detection":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "fonts":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "original_document_present": {
               "properties": {
                     "scan": "clear",
                     "document_on_printed_paper": "consider",
                     "screenshot": "clear",
                     "photo_of_screen": "consider"
               },
               "result": "clear"
             },
            "other":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "picture_face_integrity":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "security_features":{
               "properties":{
                  
               },
               "result":"clear"
            },
            "template":{
               "properties":{
                  
               },
               "result":"clear"
            }
         },
         "result":"clear"
      }
   },
   "check_id":"<CHECK_ID>",
   "created_at":"2021-03-22T17:13:12Z",
   "documents":[
      {
         "id":"<DOCUMENT_ID>"
      }
   ],
   "href":"/v3.6/reports/<REPORT_ID>",
   "id":"<REPORT_ID>",
   "name":"document",
   "properties":{
      "date_of_birth":"1990-01-01",
      "date_of_expiry":"2030-01-01",
      "document_numbers":[
         {
            "type":"document_number",
            "value":"999999999"
         }
      ],
      "document_type":"passport",
      "first_name":"Jane",
      "gender":"",
      "issuing_country":"GBR",
      "last_name":"Doe",
      "nationality":""
   },
   "result":"clear",
   "status":"complete",
   "sub_result":"clear"
}
"""

document_report = json.loads(document_report)

digital_document = document_report["breakdown"]["image_integrity"]["breakdown"]["conclusive_document_quality"]["properties"].get("digital_document")
corner_removed = document_report["breakdown"]["image_integrity"]["breakdown"]["conclusive_document_quality"]["properties"].get("corner_removed")
watermarks_digital_text_overlay = document_report["breakdown"]["image_integrity"]["breakdown"]["conclusive_document_quality"]["properties"].get("watermarks_digital_text_overlay")
obscured_security_features = document_report["breakdown"]["image_integrity"]["breakdown"]["conclusive_document_quality"]["properties"].get("obscured_security_features")

screenshot = document_report["breakdown"]["visual_authenticity"]["breakdown"]["original_document_present"]["properties"].get("screenshot")
document_on_printed_paper = document_report["breakdown"]["visual_authenticity"]["breakdown"]["original_document_present"]["properties"].get("document_on_printed_paper")
photo_of_screen = document_report["breakdown"]["visual_authenticity"]["breakdown"]["original_document_present"]["properties"].get("photo_of_screen")
scan = document_report["breakdown"]["visual_authenticity"]["breakdown"]["original_document_present"]["properties"].get("scan")

data_consistency = document_report["breakdown"]["data_consistency"]["result"]
data_comparison = document_report["breakdown"]["data_comparison"]["result"]

sub_result = 'clear'

if data_consistency == 'consider' or data_comparison == 'consider':
    sub_result = 'caution'

consider_count = sum(value == 'consider' for value in [digital_document, corner_removed, watermarks_digital_text_overlay, obscured_security_features, screenshot, document_on_printed_paper, photo_of_screen, scan])
print(f"count: {consider_count}")
print(sub_result)
