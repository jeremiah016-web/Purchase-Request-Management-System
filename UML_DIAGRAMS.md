# UML Diagrams - Purchase Request Management System

## 1. Class Diagram

```mermaid
classDiagram
    class User {
        +int id
        +string username
        +string email
        +string password
        +datetime date_joined
    }
    
    class Profile {
        +int id
        +ImageField image
        +string role
        +is_admin() bool
        +is_buyer() bool
        +is_requester() bool
        +is_vendor() bool
        +save()
    }
    
    class PR {
        +string pr_number
        +string item_type
        +text items_description
        +string quantity
        +text specifications
        +float estimated_price
        +text quotation_notes
        +datetime quotation_date
        +float total
        +bool price_approved
        +datetime price_approved_date
        +string status
        +string category
        +text description
        +datetime date_posted
        +string vendor_name
        +string vendor_contact
        +string payment_status
        +date payment_date
        +text payment_notes
        +string delivery_status
        +get_absolute_url() string
        +total_paid() float
        +remaining_balance() float
        +has_quotation() bool
    }
    
    class Vendor {
        +int id
        +string name
        +string contact_person
        +string email
        +string phone
        +text address
        +string website
        +string tax_id
        +string bank_account
        +string payment_terms
        +string categories
        +string status
        +float rating
        +bool is_approved
        +datetime approved_date
        +datetime date_added
        +text notes
        +get_absolute_url() string
        +total_orders() int
        +total_value() float
        +get_categories_list() list
        +set_categories_list(list)
    }
    
    class VendorQuotation {
        +int id
        +float estimated_price
        +text quotation_notes
        +datetime quotation_date
        +bool is_selected
        +datetime selected_date
    }
    
    class VendorContact {
        +int id
        +string contact_type
        +string subject
        +text message
        +text response
        +datetime contact_date
        +date follow_up_date
    }
    
    class Payment {
        +int id
        +float amount
        +string payment_method
        +date payment_date
        +string reference_number
        +string status
        +text notes
        +datetime created_at
    }
    
    class Delivery {
        +int id
        +string tracking_number
        +string carrier
        +string status
        +date shipped_date
        +date expected_delivery_date
        +date actual_delivery_date
        +text delivery_address
        +string recipient_name
        +string recipient_contact
        +text notes
        +datetime created_at
        +is_delayed() bool
    }
    
    User "1" -- "1" Profile : has
    User "1" -- "0..*" PR : creates
    User "1" -- "0..1" Vendor : vendor_profile
    User "1" -- "0..*" Vendor : approves
    User "1" -- "0..*" Vendor : adds
    User "1" -- "0..*" PR : submits_quotation
    User "1" -- "0..*" PR : approves_price
    User "1" -- "0..*" VendorQuotation : selects
    User "1" -- "0..*" VendorContact : contacts
    User "1" -- "0..*" Payment : processes
    User "1" -- "0..*" Delivery : creates
    
    Vendor "0..1" -- "0..*" PR : assigned_to
    Vendor "1" -- "0..*" VendorQuotation : submits
    Vendor "1" -- "0..*" VendorContact : receives
    Vendor "0..1" -- "0..*" Payment : receives_payment
    Vendor "0..1" -- "0..*" Delivery : ships
    
    PR "1" -- "0..*" VendorQuotation : has
    PR "1" -- "0..*" VendorContact : related_to
    PR "1" -- "0..*" Payment : has
    PR "1" -- "0..*" Delivery : has
```

## 2. Use Case Diagram

```mermaid
graph TB
    subgraph System["Purchase Request Management System"]
        UC1[Create Purchase Request]
        UC2[View Purchase Requests]
        UC3[Update Purchase Request]
        UC4[Delete Purchase Request]
        UC5[Submit Quotation]
        UC6[Approve/Reject PR]
        UC7[Assign Vendor]
        UC8[Approve Price]
        UC9[Manage Vendors]
        UC10[Track Payments]
        UC11[Track Deliveries]
        UC12[View Dashboard]
        UC13[Search PRs]
        UC14[Manage Profile]
        UC15[Contact Vendor]
    end
    
    Requester((Requester))
    Buyer((Buyer))
    Vendor((Vendor))
    Admin((Admin))
    
    Requester --> UC1
    Requester --> UC2
    Requester --> UC3
    Requester --> UC4
    Requester --> UC12
    Requester --> UC13
    Requester --> UC14
    
    Buyer --> UC2
    Buyer --> UC6
    Buyer --> UC7
    Buyer --> UC8
    Buyer --> UC9
    Buyer --> UC10
    Buyer --> UC11
    Buyer --> UC12
    Buyer --> UC13
    Buyer --> UC14
    Buyer --> UC15
    
    Vendor --> UC2
    Vendor --> UC5
    Vendor --> UC12
    Vendor --> UC13
    Vendor --> UC14
    
    Admin --> UC2
    Admin --> UC3
    Admin --> UC4
    Admin --> UC6
    Admin --> UC7
    Admin --> UC8
    Admin --> UC9
    Admin --> UC10
    Admin --> UC11
    Admin --> UC12
    Admin --> UC13
    Admin --> UC14
    Admin --> UC15
```

## 3. Sequence Diagram - Create Purchase Request

```mermaid
sequenceDiagram
    actor Requester
    participant UI as Web Interface
    participant View as PRCreateView
    participant Model as PR Model
    participant DB as Database
    
    Requester->>UI: Navigate to Create PR
    UI->>View: GET /pr/new/
    View->>View: Check user role
    View->>UI: Display PR form
    
    Requester->>UI: Fill form & Submit
    UI->>View: POST /pr/new/
    View->>View: Validate form data
    View->>Model: Create PR instance
    Model->>Model: Set author = current user
    Model->>Model: Set status = 'Open'
    Model->>Model: Set total = 0.00
    Model->>DB: Save PR
    DB-->>Model: Confirm save
    Model-->>View: Return PR object
    View->>UI: Redirect to PR detail
    UI-->>Requester: Show success message
```

## 4. Sequence Diagram - Vendor Quotation Submission

```mermaid
sequenceDiagram
    actor Vendor
    participant UI as Web Interface
    participant View as PRUpdateView
    participant PRModel as PR Model
    participant QuotModel as VendorQuotation Model
    participant DB as Database
    
    Vendor->>UI: Navigate to PR
    UI->>View: GET /pr/<id>/update/
    View->>View: Check vendor permissions
    View->>UI: Display quotation form
    
    Vendor->>UI: Enter price & notes
    UI->>View: POST /pr/<id>/update/
    View->>View: Validate form
    View->>QuotModel: Create/Update VendorQuotation
    QuotModel->>DB: Save quotation
    DB-->>QuotModel: Confirm save
    View->>PRModel: Update legacy fields
    PRModel->>DB: Save PR
    DB-->>PRModel: Confirm save
    View->>UI: Redirect to PR detail
    UI-->>Vendor: Show success message
```

## 5. Sequence Diagram - Buyer Approval Process

```mermaid
sequenceDiagram
    actor Buyer
    participant UI as Web Interface
    participant View as PRUpdateView
    participant PRModel as PR Model
    participant QuotModel as VendorQuotation Model
    participant DB as Database
    
    Buyer->>UI: View PR with quotations
    UI->>View: GET /pr/<id>/update/
    View->>QuotModel: Fetch all quotations
    QuotModel->>DB: Query quotations
    DB-->>QuotModel: Return quotations
    View->>UI: Display PR with quotations
    
    Buyer->>UI: Select vendor & approve price
    UI->>View: POST /pr/<id>/update/
    View->>QuotModel: Mark quotation as selected
    QuotModel->>DB: Update is_selected = True
    View->>PRModel: Set vendor & total
    View->>PRModel: Set price_approved = True
    View->>PRModel: Update status to 'Approval'
    PRModel->>DB: Save PR
    DB-->>PRModel: Confirm save
    View->>UI: Redirect to PR detail
    UI-->>Buyer: Show success message
```

## 6. Activity Diagram - Purchase Request Workflow

```mermaid
flowchart TD
    Start([Start]) --> CreatePR[Requester Creates PR]
    CreatePR --> SetOpen[Status: Open]
    SetOpen --> BuyerReview{Buyer Reviews}
    
    BuyerReview -->|Reject| SetClosed[Status: Closed]
    SetClosed --> End([End])
    
    BuyerReview -->|Approve| SetPending[Status: Pending]
    SetPending --> VendorView[Vendors View PR]
    VendorView --> SubmitQuote[Vendors Submit Quotations]
    
    SubmitQuote --> BuyerSelect{Buyer Selects Vendor}
    BuyerSelect -->|No suitable vendor| SetOnHold[Status: On Hold]
    SetOnHold --> End
    
    BuyerSelect -->|Select vendor| ApprovePrice[Approve Price]
    ApprovePrice --> SetApproval[Status: Approval]
    SetApproval --> ProcessPayment[Process Payment]
    
    ProcessPayment --> UpdatePaymentStatus{Payment Complete?}
    UpdatePaymentStatus -->|Partial| PartialPaid[Payment Status: Partially Paid]
    PartialPaid --> ProcessPayment
    UpdatePaymentStatus -->|Complete| FullPaid[Payment Status: Paid]
    
    FullPaid --> ArrangeDelivery[Arrange Delivery]
    ArrangeDelivery --> ShipItems[Status: In Transit]
    ShipItems --> DeliverItems[Status: Delivered]
    DeliverItems --> ClosePR[Status: Closed]
    ClosePR --> End
```

## 7. State Chart Diagram - PR Status

```mermaid
stateDiagram-v2
    [*] --> Open: Requester creates PR
    
    Open --> Pending: Buyer reviews & approves
    Open --> Closed: Buyer rejects
    
    Pending --> OnHold: No suitable vendor
    Pending --> Approval: Buyer selects vendor & approves price
    
    OnHold --> Pending: Issue resolved
    OnHold --> Closed: Cancelled
    
    Approval --> Closed: Payment complete & delivered
    
    Closed --> [*]
    
    note right of Open
        Initial state
        Requester can edit
    end note
    
    note right of Pending
        Waiting for vendor quotations
        Vendors can submit quotes
    end note
    
    note right of Approval
        Price approved
        Processing payment & delivery
    end note
    
    note right of OnHold
        Temporary hold
        Awaiting resolution
    end note
    
    note right of Closed
        Final state
        PR completed or cancelled
    end note
```

## 8. Deployment Diagram

```mermaid
graph TB
    subgraph "Client Tier"
        Browser[Web Browser]
    end
    
    subgraph "Application Server"
        Django[Django Application Server]
        StaticFiles[Static Files Server]
        MediaFiles[Media Files Server]
    end
    
    subgraph "Data Tier"
        SQLite[(SQLite Database)]
        FileSystem[File System<br/>Profile Images]
    end
    
    Browser -->|HTTPS| Django
    Browser -->|HTTP| StaticFiles
    Browser -->|HTTP| MediaFiles
    
    Django -->|SQL Queries| SQLite
    Django -->|Read/Write| FileSystem
    MediaFiles -->|Serve| FileSystem
    
    style Browser fill:#e1f5ff
    style Django fill:#ffe1e1
    style SQLite fill:#e1ffe1
    style FileSystem fill:#fff4e1
```

## 9. Component Diagram

```mermaid
graph TB
    subgraph "Django Project"
        subgraph "Users App"
            UserModels[User Models<br/>Profile, ROLE_CHOICES]
            UserViews[User Views<br/>Register, Profile, Delete]
            UserForms[User Forms<br/>Registration, Update]
            UserMixins[User Mixins<br/>Role-based Access Control]
        end
        
        subgraph "PRS App"
            PRModels[PR Models<br/>PR, Vendor, Payment, Delivery]
            PRViews[PR Views<br/>CRUD, Dashboard, Search]
            PRTemplates[PR Templates<br/>HTML Templates]
            PRStatic[PR Static<br/>CSS, JS]
        end
        
        subgraph "Django Core"
            Auth[Authentication]
            ORM[ORM/Models]
            Templates[Template Engine]
            Static[Static Files]
        end
        
        subgraph "Third Party"
            CrispyForms[Crispy Forms]
            Pillow[Pillow<br/>Image Processing]
            AllAuth[Django AllAuth<br/>Social Auth]
        end
    end
    
    UserViews --> UserModels
    UserViews --> UserForms
    UserViews --> Auth
    UserModels --> ORM
    UserModels --> Pillow
    
    PRViews --> PRModels
    PRViews --> UserMixins
    PRViews --> PRTemplates
    PRModels --> ORM
    PRTemplates --> Templates
    PRTemplates --> CrispyForms
    PRStatic --> Static
    
    UserViews --> AllAuth
    
    style UserModels fill:#ffe1e1
    style PRModels fill:#e1f5ff
    style Auth fill:#e1ffe1
    style ORM fill:#fff4e1
```

## 10. Collaboration Diagram - PR Creation

```mermaid
graph LR
    Requester[":Requester"]
    UI[":WebInterface"]
    View[":PRCreateView"]
    Form[":PRForm"]
    Model[":PR"]
    DB[":Database"]
    
    Requester -->|1: navigate to create PR| UI
    UI -->|2: GET request| View
    View -->|3: check role| View
    View -->|4: create form| Form
    Form -->|5: return form| View
    View -->|6: render form| UI
    UI -->|7: display form| Requester
    
    Requester -->|8: submit data| UI
    UI -->|9: POST request| View
    View -->|10: validate| Form
    Form -->|11: validation result| View
    View -->|12: create instance| Model
    Model -->|13: set defaults| Model
    Model -->|14: save| DB
    DB -->|15: confirm| Model
    Model -->|16: return object| View
    View -->|17: redirect| UI
    UI -->|18: show success| Requester
```

## 11. Object Diagram - PR with Quotations

```mermaid
graph TB
    subgraph "Purchase Request Instance"
        PR1["pr1: PR<br/>pr_number='PR-2024-001'<br/>status='Pending'<br/>category='IT'<br/>total=0.00"]
    end
    
    subgraph "User Instances"
        User1["user1: User<br/>username='john_requester'<br/>role='requester'"]
        User2["user2: User<br/>username='jane_buyer'<br/>role='buyer'"]
    end
    
    subgraph "Vendor Instances"
        Vendor1["vendor1: Vendor<br/>name='Tech Solutions'<br/>status='Active'<br/>rating=4.5"]
        Vendor2["vendor2: Vendor<br/>name='IT Services Inc'<br/>status='Active'<br/>rating=4.2"]
    end
    
    subgraph "Quotation Instances"
        Quote1["quote1: VendorQuotation<br/>estimated_price=5000.00<br/>is_selected=false"]
        Quote2["quote2: VendorQuotation<br/>estimated_price=4500.00<br/>is_selected=true"]
    end
    
    PR1 -.->|author| User1
    PR1 -.->|vendor| Vendor2
    
    Quote1 -.->|pr| PR1
    Quote1 -.->|vendor| Vendor1
    
    Quote2 -.->|pr| PR1
    Quote2 -.->|vendor| Vendor2
    Quote2 -.->|selected_by| User2
```

## Summary

These UML diagrams provide a comprehensive view of the Purchase Request Management System:

1. **Class Diagram**: Shows the complete data model with all entities and relationships
2. **Use Case Diagram**: Illustrates system functionality from different user perspectives
3. **Sequence Diagrams**: Detail the interaction flow for key processes
4. **Activity Diagram**: Maps the complete PR workflow from creation to completion
5. **State Chart Diagram**: Shows PR status transitions and conditions
6. **Deployment Diagram**: Illustrates the system architecture and deployment structure
7. **Component Diagram**: Shows the modular structure and dependencies
8. **Collaboration Diagram**: Details object interactions during PR creation
9. **Object Diagram**: Shows a snapshot of system objects and their relationships

These diagrams can be rendered using Mermaid-compatible tools or viewers.
ca