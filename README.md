# poc-observability-tracker


python3 -m venv venv
source venv/bin/activate

pip install -r reuirements.txt
pip freeze

uvicorn main:app --reload


sample JSON body

{
  "nodes": [
    "string"
  ],
  "edges": [
    {
      "from": "Web/mobile",
      "to": "string"
    }
  ]
}



other request 

{
  "nodes": [
    "Web/mobile",
    "Akamani/CDN",
    "Gateway",
    "UI sdk",
    "Authentication",
    "Internal Services",
    "External Service",
    "DB check for credentials"
  ],
  "edges": [
    { "from": "Web/mobile", "to": "Akamani/CDN" },
    { "from": "Akamani/CDN", "to": "Gateway" },
    { "from": "Gateway", "to": "UI sdk" },
    { "from": "Gateway", "to": "Authentication" },
    { "from": "Authentication", "to": "Internal Services" },
    { "from": "Authentication", "to": "External Service" },
    { "from": "Internal Services", "to": "DB check for credentials" },
    { "from": "External Service", "to": "DB check for credentials" }
  ]
}


To check the DAG graph 

please pass these as the inputs in the swagger as 

visualization as True 
output as table

it will save the image 