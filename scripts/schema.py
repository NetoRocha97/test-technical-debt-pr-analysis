ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {

        "repo": {
            "type": "string"
        },

        "pr_number": {
            "type": "integer"
        },

        "primary_pr_objective": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "enum": ["BUG", "IMP", "REQ", "NONE"]
                },
                "evidence": {
                    "type": "array",
                    "items": {
                        "$ref": "#/$defs/evidence"
                    }
                }
            },
            "required": ["value", "evidence"],
            "additionalProperties": False
        },

        "suggestion_type": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "enum": ["EXPLICIT", "IMPLICIT", "NONE"]
                },
                "evidence": {
                    "type": "array",
                    "items": {
                        "$ref": "#/$defs/evidence"
                    }
                }
            },
            "required": ["value", "evidence"],
            "additionalProperties": False
        },

        "agreement": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "enum": [
                        "AGREED",
                        "REJECTED",
                        "POSTPONED",
                        "IGNORED",
                        "UNKNOWN"
                    ]
                },
                "evidence": {
                    "type": "array",
                    "items": {
                        "$ref": "#/$defs/evidence"
                    }
                }
            },
            "required": ["value", "evidence"],
            "additionalProperties": False
        },

        "resolution": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "enum": [
                        "FIXED",
                        "P-FIXED",
                        "UNFIXED",
                        "NONE",
                        "UNKNOWN"
                    ]
                },
                "evidence": {
                    "type": "array",
                    "items": {
                        "$ref": "#/$defs/evidence"
                    }
                }
            },
            "required": ["value", "evidence"],
            "additionalProperties": False
        },

        "test_td_mentioned": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "enum": ["YES", "NO"]
                },
                "evidence": {
                    "type": "array",
                    "items": {
                        "$ref": "#/$defs/evidence"
                    }
                }
            },
            "required": ["value", "evidence"],
            "additionalProperties": False
        },

        "mention_type": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "enum": [
                        "EXPLICIT",
                        "IMPLICIT",
                        "NOT_APPLICABLE"
                    ]
                },
                "evidence": {
                    "type": "array",
                    "items": {
                        "$ref": "#/$defs/evidence"
                    }
                }
            },
            "required": ["value", "evidence"],
            "additionalProperties": False
        },

        "test_td_type": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "enum": [
                        "FRAGILE_TEST",
                        "HARD_TO_MAINTAIN_TEST",
                        "LOW_COVERAGE",
                        "MISSING_TEST",
                        "BROKEN_TEST",
                        "SLOW_TEST",
                        "ENVIRONMENT_DEPENDENCY",
                        "OUTDATED_TEST",
                        "TEST_DESIGN",
                        "TEST_DATA",
                        "WEAK_INSUFFICIENT_ASSERTION",
                        "UNNECESSARY_REDUNDANT_TEST_CODE",
                        "FLAKY_TEST",
                        "TEST_COMPATIBILITY",
                        "TEST_STABILITY",
                        "TEST_CLEANUP",
                        "OTHER",
                        "NOT_APPLICABLE"
                    ]
                },
                "evidence": {
                    "type": "array",
                    "items": {
                        "$ref": "#/$defs/evidence"
                    }
                }
            },
            "required": ["value", "evidence"],
            "additionalProperties": False
        },

        "sonarqube_rules_discussed": {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {

            "rule": {
                "type": "string"
            },

            "mentioned": {
                "type": "boolean"
            },

            "mention_type": {
                "type": "string",
                "enum": [
                    "EXPLICIT",
                    "IMPLICIT",
                    "NOT_APPLICABLE"
                ]
            },

            "relationship": {
                "type": "string",
                "enum": [
                    "SAME",
                    "COMPLEMENTARY",
                    "DIFFERENT",
                    "NOT_DISCUSSED"
                ]
            },

            "evidence": {
                "type": "array",
                "items": {
                    "$ref": "#/$defs/evidence"
                }
            }

        },
        "required": [
            "rule",
            "mentioned",
            "mention_type",
            "relationship",
            "evidence"
        ],
        "additionalProperties": False
        }
    }

    },

    "$defs": {

        "evidence": {
            "type": "object",
            "properties": {

                "comment_id": {
                    "type": "integer"
                },

                "author": {
                    "type": "string"
                },

                "comment": {
                    "type": "string"
                }

            },
            "required": [
                "comment_id",
                "author",
                "comment"
            ],
            "additionalProperties": False
        }

    },

    "required": [
        "repo",
        "pr_number",
        "primary_pr_objective",
        "suggestion_type",
        "agreement",
        "resolution",
        "test_td_mentioned",
        "mention_type",
        "test_td_type",
        "sonarqube_rules_discussed"
    ],

    "additionalProperties": False
}

RESPONSE_FORMAT = {
    "type": "json_schema",
    "name": "pr_analysis",
    "strict": True,
    "schema": ANALYSIS_SCHEMA,
}
