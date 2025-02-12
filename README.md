# Resume Parsing and LLM Interaction System

## Overview

This project implements a system for parsing resumes using OCR and interacting with a Large Language Model (LLM) to extract and process resume data. The architecture is designed for local deployment and utilizes Docker Compose for easy setup and containerization of all components.

The system comprises the following main components, as visualized in the architecture diagram:

*   **Streamlit Webpage:** Provides a user-friendly web interface for uploading resumes and interacting with the system.
*   **Python Backend:**  Serves as the core logic and orchestration layer, connecting the frontend with the backend services.
*   **FastAPI APIs:**  Two FastAPI instances are used:
    *   **Resume Parser API:**  Handles communication with the OCR Resume Parser.
    *   **LLM API:**  Provides an interface to interact with the LLama 3.1 LLM.
*   **OCR Resume Parser:**  A dedicated service responsible for performing Optical Character Recognition (OCR) on uploaded resume documents to extract text.
*   **LLama 3.1 LLM:**  The Large Language Model used for processing and analyzing the parsed resume text.
*   **MongoDB Database:**  A database used to store and manage parsed resume data.
*   **Database Monitoring:**  A tool for monitoring the MongoDB database.
*   **Docker Compose:**  Docker Compose is the primary tool for running the entire system. It manages the containerization and orchestration of all components.

## Architecture Diagram

![image](https://github.com/user-attachments/assets/8c7c7c75-b459-4802-ade5-d5e8e2a27435)



## Getting Started

Follow these steps to set up and run the Resume Parsing and LLM Interaction System locally using Docker Compose.

### Prerequisites

*   **Docker and Docker Compose:** Ensure you have Docker and Docker Compose installed on your system. You can download them from [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone git@github.com:melekmsakni/dashboard_streamlit.git
    cd dashboard_streamlit
    ```

    *(Replace `[repository-url]` with the actual URL of your GitHub repository and `[repository-directory]` with the cloned directory name).*

2.  **Docker Compose:**

    This project is designed to be run using Docker Compose. Ensure you have a `docker-compose.yml` file in the root directory of the repository. No further installation steps are typically required beyond having Docker and Docker Compose installed.

### Running the Application

**Using Docker Compose (Recommended and Only Method):**

1.  **Start the System:**

    Navigate to the repository root directory (where `docker-compose.yml` is located) and run:

    ```bash
    docker-compose up --build
    ```

    This command will build all Docker images (if necessary) and start all services defined in your `docker-compose.yml` file. This single command sets up and runs the entire application stack.

2.  **Access the Streamlit Webpage:**

    Once the services are running, open your web browser and go to the address where the Streamlit application is served (e.g., `http://localhost:8501` - check your Streamlit application logs for the exact address if different).

### Usage

1.  **Access the Webpage:** Open the Streamlit webpage in your browser.
2.  **Upload Resume:** Use the interface provided by the Streamlit application to upload a resume file.
3.  **View Parsed Data:** The system will process the resume:
    *   The **OCR Resume Parser** will extract text from the document.
    *   The **LLama 3.1 LLM** will process the text.
    *   The parsed and processed data will be displayed on the **Streamlit Webpage**.
4.  **Interact with the LLM (if implemented):** Depending on the application's features, you may be able to interact with the LLM through the webpage.
5.  **Database Monitoring (Optional):** Use the Database Monitoring tool (access instructions depend on the specific tool) to observe the MongoDB database.

## Tools and Technologies

*   **Frontend:** Streamlit (Python)
*   **Backend (Core Logic):** Python
*   **API Framework:** FastAPI (Python)
*   **Large Language Model (LLM):** Llama 3.1 (Meta)
*   **OCR:** [Specify the OCR library or service used if known]
*   **Database:** MongoDB
*   **Containerization & Orchestration:** Docker Compose

## License

[Specify the License for your project, e.g., MIT License, Apache 2.0, GPL, or "No License"]

## Contact

[Your Name/Team Name]
[Your Email or Contact Information (Optional)]
