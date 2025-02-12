# dashboard_streamlit


# Resume Parsing and LLM Interaction System

## Overview

This project implements a system for parsing resumes using OCR and interacting with a Large Language Model (LLM) to extract and process resume data. The architecture is designed for local deployment and utilizes Docker for containerization of key components.

The system comprises the following main components, as visualized in the architecture diagram:

*   **Streamlit Webpage:** Provides a user-friendly web interface for uploading resumes and interacting with the system.
*   **Python Backend:**  Serves as the core logic and orchestration layer, connecting the frontend with the backend services.
*   **FastAPI APIs:**  Two FastAPI instances are used:
    *   **Resume Parser API:**  Handles communication with the OCR Resume Parser.
    *   **LLM API:**  Provides an interface to interact with the LLama 3.1 LLM.
*   **OCR Resume Parser:**  A dedicated service responsible for performing Optical Character Recognition (OCR) on uploaded resume documents to extract text.
*   **LLama 3.1 LLM:**  The Large Language Model used for processing and analyzing the parsed resume text (e.g., information extraction, summarization, etc.).
*   **MongoDB Database:**  A database used to store and manage parsed resume data and potentially other system-related information.
*   **Database Monitoring:**  A tool for monitoring the MongoDB database, ensuring its health and performance.
*   **Docker:**  Docker is used to containerize several components (Resume Parser, LLM, FastAPI APIs, Database Monitoring, and Database itself), simplifying deployment and ensuring consistent environments.

## Architecture Diagram

![image](https://github.com/user-attachments/assets/cb95b1a4-95f6-457f-97b3-a2ffefb514d4)

*(Replace `link-to-your-architecture-diagram-image-or-replace-with-instructions-to-view-diagram` above with a direct link to an image of your architecture diagram if you have one online, or provide instructions on how to view the diagram file if it's included in the repository. If you generated the diagram using a tool, you might be able to export it as an image).*

**Alternatively, if you cannot easily include an image, describe the diagram visually:**

> The architecture diagram visually represents the data flow as follows:
>
> 1.  A user interacts with the **Streamlit Webpage** to upload a resume.
> 2.  The **Streamlit** application, built with **Python**, sends the resume to the **Resume Parser API** (FastAPI, Dockerized).
> 3.  The **Resume Parser API** communicates with the **OCR Resume Parser** (Dockerized) to extract text from the resume.
> 4.  The parsed text is then sent back to the **Python Backend**.
> 5.  The **Python Backend** might store the parsed data in the **MongoDB Database** (Dockerized).
> 6.  For LLM processing, the **Python Backend** sends the parsed resume text to the **LLM API** (FastAPI, Dockerized), interacting with the **LLama 3.1 LLM** (Dockerized).
> 7.  The **LLM API** returns the processed information from the LLM back to the **Python Backend** and subsequently to the **Streamlit Webpage** for the user to view.
> 8.  **Database Monitoring** (Dockerized) is used to observe the **MongoDB Database**.
>
> Docker containers are indicated for components like FastAPI APIs, OCR Resume Parser, LLama 3.1, MongoDB, and Database Monitoring.

## Getting Started

Follow these steps to set up and run the Resume Parsing and LLM Interaction System locally.

### Prerequisites

*   **Docker and Docker Compose:** Ensure you have Docker and Docker Compose installed on your system. You can download them from [Docker Desktop](https://www.docker.com/products/docker-desktop/).
*   **Python 3.10:** Python 3.x is required to run the Streamlit frontend and potentially for custom backend scripts if not fully containerized.
*   **[Optional] Virtual Environment (venv or conda):**  Recommended for managing Python dependencies.

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone [repository-url]
    cd [repository-directory]
    ```

    *(Replace `[repository-url]` with the actual URL of your GitHub repository and `[repository-directory]` with the cloned directory name).*

2.  **Set up Python Environment (for Streamlit Frontend and potential backend scripts):**

    If you plan to run the Streamlit frontend or any Python backend components directly (outside of Docker), create a virtual environment (optional but recommended):

    ```bash
    # Using venv (for example)
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate  # On Windows

    # Or using conda
    conda create -n myenv python=3.x
    conda activate myenv
    ```

    Install Python dependencies (if any are listed in `requirements.txt` or similar):

    ```bash
    pip install -r requirements.txt  # If you have a requirements.txt file
    ```

    *(If you have specific Python dependencies for the Streamlit frontend or any other Python components outside Docker, list them in a `requirements.txt` file and install them here).*

3.  **Docker Compose (Recommended for easy setup):**

    This project is designed to be easily run using Docker Compose. Ensure you have a `docker-compose.yml` file in the root directory of the repository.

### Running the Application

**Using Docker Compose (Recommended):**

1.  **Start the System:**

    Navigate to the repository root directory (where `docker-compose.yml` is located) and run:

    ```bash
    docker-compose up --build
    ```

    This command will build all Docker images (if necessary) and start all services defined in your `docker-compose.yml` file (including the FastAPI APIs, OCR Parser, LLama LLM, MongoDB, and Database Monitoring).

2.  **Access the Streamlit Webpage:**

    Once the services are running, open your web browser and go to the address where the Streamlit application is served (e.g., `http://localhost:8501` - check your Streamlit application logs for the exact address if different).

**Running Components Individually (Less Recommended, for development or troubleshooting):**

If you need to run components individually (e.g., for development or debugging), you would need to:

1.  **Build Docker Images:**

    Navigate to the directory of each Dockerized component (e.g., `resume-parser-api`, `llm-api`, `ocr-parser`, `mongodb`, `database-monitoring`) and build their Docker images:

    ```bash
    docker build -t [image-name] .
    ```

    *(Replace `[image-name]` with a suitable name for each image, e.g., `resume-parser-api-image`, `llm-api-image`, etc.)*

2.  **Run Docker Containers:**

    Run each Docker container individually, ensuring they are properly linked and configured to communicate with each other.  You'll need to refer to the Dockerfiles and any specific instructions for each component to determine the correct `docker run` commands, port mappings, environment variables, and network settings.

3.  **Run Streamlit Frontend (if not Dockerized):**

    If your Streamlit frontend is not containerized, navigate to the Streamlit application directory and run it:

    ```bash
    streamlit run your_streamlit_app.py
    ```

    *(Replace `your_streamlit_app.py` with the actual filename of your Streamlit application script).*

### Usage

1.  **Access the Webpage:** Open the Streamlit webpage in your browser.
2.  **Upload Resume:** Use the interface provided by the Streamlit application to upload a resume file (e.g., PDF, DOCX, image).
3.  **View Parsed Data:** The system will process the resume:
    *   The **OCR Resume Parser** will extract text from the document.
    *   The **LLama 3.1 LLM** will process the text (depending on the implemented functionality, this could include extracting key information, summarizing skills, etc.).
    *   The parsed and processed data will be displayed on the **Streamlit Webpage**.
4.  **Interact with the LLM (if implemented):** Depending on the features of the application, you might be able to interact with the LLM through the webpage to ask questions about the resume or perform further analysis.
5.  **Database Monitoring (Optional):** Use the Database Monitoring tool (access instructions will depend on the tool used - often a web interface) to monitor the MongoDB database and verify that parsed resume data is being stored correctly.

## Tools and Technologies

*   **Frontend:** Streamlit (Python)
*   **Backend (Core Logic):** Python
*   **API Framework:** FastAPI (Python)
*   **Large Language Model (LLM):** Llama 3.1 (Meta)
*   **OCR:** [Specify the OCR library or service used if known, e.g., Tesseract OCR, Google Cloud Vision API, etc.]
*   **Database:** MongoDB
*   **Containerization:** Docker
*   **Orchestration (optional, if using Docker Compose):** Docker Compose
*   **Database Monitoring:** [Specify the Database Monitoring Tool used if known, e.g., MongoDB Compass, pgAdmin, etc.]

## License

[Specify the License for your project, e.g., MIT License, Apache 2.0, GPL, or "No License"]

## Contact

[Your Name/Team Name]
[Your Email or Contact Information (Optional)]

---

**Note:**

*   Remember to replace the bracketed placeholders (e.g., `[repository-url]`, `[repository-directory]`, `link-to-your-architecture-diagram-image-or-replace-with-instructions-to-view-diagram]`, `[image-name]`, etc.) with the actual information for your project.
*   If you used a specific OCR library or Database Monitoring tool, replace the placeholders in the "Tools and Technologies" section with the correct names.
*   If you have a `requirements.txt` file or other specific installation instructions, make sure to include them in the "Installation" section.
*   If you are using Docker Compose, ensure you have a `docker-compose.yml` file in your repository and that it correctly defines all the services.
*   Adjust the "Usage" section to accurately reflect the features and user interaction flow of your application.
*   Consider adding sections on "Contributing," "Roadmap," or "Credits" if relevant to your project.
*   You can further enhance this README with badges (e.g., build status, license badge) if you are using platforms like GitHub Actions or have a license file.

This README file should provide a good starting point for users to understand, set up, and run your Resume Parsing and LLM Interaction System. Good luck!
