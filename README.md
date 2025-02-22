This project is a proof of concept for assessing manpower requirements in Coal India mines, taking into account established standards for various job roles.  It's built using Django and SQLite, providing a web-based interface for managing job roles, standards, and calculating required manpower.

## Introduction

Efficient manpower planning is crucial for the smooth operation of coal mines. This project aims to demonstrate how a Django-based application can be used to streamline this process.  It provides a centralized platform to define job roles, their associated standard manpower requirements (e.g., number of workers per shift, qualifications, etc.), and then use this data to calculate the overall manpower needed for a given mine or project. This proof of concept focuses on demonstrating the core logic and data management aspects.

## Features

*   **Job Role Management:**  Define and manage various job roles within the mine (e.g., Miner, Supervisor, Engineer).  Includes fields for job title, description, required skills, and any other relevant attributes.
*   **Standard Definition:** For each job role, define the standard manpower requirements. This could include the number of personnel required per shift, required qualifications, experience levels, etc.
*   **Manpower Calculation:**  Based on the defined job roles and standards, the application can calculate the total manpower required for a given mine or project.  This calculation can be based on factors such as production targets, number of shifts, or other user-defined parameters.
*   **Data Storage:** Uses SQLite for data storage, simplifying setup and deployment for this proof of concept.
*   **Web Interface:**  Provides a user-friendly web interface built with Django for managing job roles, standards, and performing calculations.


## Technologies Used

*   Python
*   Django
*   SQLite
