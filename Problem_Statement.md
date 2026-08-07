# Problem Statement

## 1. Title

**Tree Plantation Tracking Platform**

## 2. Domain

**Environmental Management / Web Application**

## 3. Who is the user? (2–3 user types, with roles)

1. **User** – Registers trees that they have planted and records their growth information.
2. **Admin** – Manages users, tree information, and plantation records.
3. **Guest** – Can view basic information about the platform without accessing private user records.

## 4. What problem are we solving?

People may plant trees but often do not maintain proper records of the trees they have planted. Information such as the planting date, location, tree type, and growth details can be difficult to track manually. This makes it difficult for users to maintain a clear history of their plantations. The proposed platform provides a simple digital way to record plantations and update their growth information over time.

## 5. Proposed Solution

The Tree Plantation Tracking Platform will provide a simple web application where users can:

* Register and log in to the system.
* Add a new tree plantation record.
* Enter basic details such as tree type, planting date, and location.
* View their planted trees.
* Update the growth information of a planted tree.
* View the plantation history and current growth records.
* Manage their own plantation records.

The admin will be able to:

* Manage registered users.
* Manage tree types.
* View and manage plantation records.
* Monitor the records stored in the system.

## 6. Core Entities / Database Tables

The system will contain the following main database tables:

1. **Users** – Stores user account information.
2. **Roles** – Stores the different roles available in the system.
3. **Trees** – Stores basic information about tree types.
4. **Plantations** – Stores information about each tree planted by a user.
5. **Growth Records** – Stores growth updates for planted trees.
6. **Locations** – Stores plantation location information.

These tables will have relationships between them, such as users having plantations and plantations having multiple growth records.

## 7. User Roles & Permissions

### User

* Register and log in.
* Add plantation records.
* View their plantation records.
* Update growth information.
* View their tree growth history.
* Manage their own records.

### Admin

* Log in to the admin section.
* View registered users.
* Manage tree types.
* View plantation records.
* Manage location information.
* Monitor growth records.

## 8. Success Criteria

The project will be considered successful when:

* A user can register and log in successfully.
* A user can add a plantation record.
* A user can view their planted trees.
* A user can add and view growth records for their trees.
* An admin can view and manage the system records.
* All important data is stored and retrieved from the database correctly.
* The application works through the deployed web application.

## 9. Out of Scope

To keep the project simple and achievable, the following will **not** be developed:

* Online payment system.
* IoT sensors for automatic tree monitoring.
* Hardware integration.
* Automatic image recognition of trees.
* Real-time GPS tracking.
* Social media features.
* Mobile application.
* Complex environmental or weather prediction.
* Advanced analytics and machine learning.

## 10. Chosen Track

**Python – FastAPI**
