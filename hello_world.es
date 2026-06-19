GET /restaurants/_search
{
    
}
"query": {
      "geo_distance": {                                                                                                                                          
        "distance": "5km",
        "location": {
          "lat": 12.97, 
          "lon": 77.59                                                                                                                                           
        }
      }                                                                                                                                                          
    } 