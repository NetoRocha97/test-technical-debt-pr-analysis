RESPONSE_FORMAT = {

    "type": "json_schema",

    "name": "rejection_reason",

    "schema": {

        "type": "object",

        "properties": {

            "repo": {
                "type": "string"
            },

            "pr_number": {
                "type": "integer"
            },

            "rejection_reason": {

                "type": "object",

                "properties": {

                    "value": {

                        "type": "string",

                        "enum": [

                            "AUTHOR_DISAGREES",

                            "OUT_OF_SCOPE",

                            "TOO_COMPLEX",

                            "ALREADY_ADDRESSED",

                            "NOT_NECESSARY",

                            "OTHER",

                            "UNKNOWN"

                        ]

                    },

                    "evidence": {

                        "type": "array",

                        "items": {

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

                    }

                },

                "required": [

                    "value",

                    "evidence"

                ],

                "additionalProperties": False

            }

        },

        "required": [

            "repo",

            "pr_number",

            "rejection_reason"

        ],

        "additionalProperties": False

    },

    "strict": True

}