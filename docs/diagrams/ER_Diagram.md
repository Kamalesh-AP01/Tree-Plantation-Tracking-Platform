erDiagram

    ROLES ||--o{ USERS : has
    USERS ||--o{ PLANTATIONS : creates
    TREES ||--o{ PLANTATIONS : planted
    LOCATIONS ||--o{ PLANTATIONS : contains
    PLANTATIONS ||--o{ GROWTH_RECORDS : has

    ROLES {
        int id
        string name
    }

    USERS {
        int id
        string name
        string email
        string password
        int role_id
    }

    TREES {
        int id
        string tree_name
    }

    LOCATIONS {
        int id
        string location_name
    }

    PLANTATIONS {
        int id
        int user_id
        int tree_id
        int location_id
        date planting_date
    }

    GROWTH_RECORDS {
        int id
        int plantation_id
        float height
        date recorded_date
    }
    