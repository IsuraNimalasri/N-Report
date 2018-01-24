analytic_good_qty= {
  "size": 0,
  "query": {
    "filtered": {
      "filter": {
        "bool": {
         "must": [
           {
             "term": {
               "factory_id": "lintimo"
             }
           },
           {"term": {
             "currentdate": "2018-01-17"
           }}
         ]
        }
      }
    }
  },
  "aggs": {
    "0": {
      "terms": {
        "field": "line_id",
        "size": 30
      },
      "aggs": {
        "1": {
          "terms": {
            "field": "fg_count",
            "size": 1,
            "order": {
              "_term": "desc"
            }
          }
        }
      }
    }
  }
}

ops_good_qty = {
  "size": 0,
  "query": {
    "filtered": {
      "filter": {
        "term": {
          "factory_id": "lintimo"
        }
      }
    }
  },
  "aggs": {
    "0": {
      "terms": {
        "field": "line_id",
        "size": 30
      },
      "aggs": {
        "1": {
          "sum": {
            "field": "value"
          }
        }
      }
    }
  }
}

qc_last_good_item_time = {
  "size": 0,
  "query": {
    "filtered": {
      "filter": {
        "term": {
          "factory_id": "lintimo"
        }
      }
    }
  },
  "aggs": {
    "0": {
      "terms": {
        "field": "line_id",
        "size": 30
      },
      "aggs": {
        "1": {
          "terms": {
            "field": "datetime",
            "size": 1,
            "order": {
              "_term": "desc"
            }
          }
        }
      }
    }
  }
}

ana_last_good_item_time = {
  "size": 0,
  "query": {
    "filtered": {
      "filter": {
        "term": {
          "factory_id": "lintimo"
        }
      }
    }
  },
  "aggs": {
    "0": {
      "terms": {
        "field": "line_id",
        "size": 30
      },
      "aggs": {
        "1": {
          "terms": {
            "field": "datetime",
            "size": 1,
            "order": {
              "_term": "desc"
            }
          }
        }
      }
    }
  }
}

Seesplan = {
  "size": 0,
  "query": {
    "filtered": {
      "filter": {
        "term": {
          "factory_id": "lintimo"
        }
      }
    }
  },
  "aggs": {
    "0": {
      "terms": {
        "field": "line_id",
        "size": 30
      },
      "aggs": {
        "1": {
          "terms": {
            "field": "sessionplanname",
            "size": 1
          }
        }
      }
    }
  }
}