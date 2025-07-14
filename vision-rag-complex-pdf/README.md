# Vision RAG App – Setup & Usage Guide

This project uses Qdrant and RunPod to run a Retrieval-Augmented Generation (RAG) application with vision capabilities. Follow the steps below to set up your environment and launch the application.

---

## 🚀 Prerequisites

- Have accounts on [Qdrant Cloud](https://cloud.qdrant.io) and [RunPod](https://www.runpod.io/)
- Have a development environment that supports remote SSH (e.g., VSCode + Remote SSH)

---

## 🔐 Environment Variable Configuration

1. Obtain the following values:

   - `QDRANT_URL` and `QDRANT_API_KEY` from Qdrant Cloud
   - `RUNPOD_API_KEY` from RunPod.io (make sure your payment credits are set)

2. Add these variables to the `.env` file in the root directory:

   ```env
   QDRANT_URL=...
   QDRANT_API_KEY=...
   RUNPOD_API_KEY=...
   ```

---

## 🛠️ Initial Setup

1. Run the following command to install dependencies and prepare the virtual environment:

   ```bash
   make pre-setup
   ```

2. Close and reopen your IDE to ensure it picks up the new virtual environment.

---

## 🔧 RunPod Setup

1. Run:

   ```bash
   make setup-pod
   ```

   This will define SSH keys and create a pod on RunPod.

2. Configure the SSH keys in your IDE if needed.

3. Open a new IDE tab connected to the remote pod via SSH.

---

## 📦 Receiving Files on the Pod

1. In the new tab connected to the remote pod, run:

   ```bash
   runpodctl receive <code>
   ```

   > Note: You can get the `<code>` from the console in your original tab.

2. Install required tools:

   ```bash
   sudo apt install sudo unzip
   ```

3. Extract the received file:

   ```bash
   unzip file.zip
   ```

---

## ⚙️ Vision RAG Setup

1. Run:

   ```bash
   make setup-vision-rag
   ```

2. Restart the IDE to apply virtual environment changes.

3. Reconnect to the remote pod using:

   ```bash
   positron --remote ssh-remote+runpod-pytorch .
   ```

---

## 🧠 Data Processing

1. Convert PDFs to PNG images:

   ```bash
   make pdf2png
   ```

2. Upload PNG images to Qdrant:

   ```bash
   make png2qdrant
   ```

3. Start the Ollama model server:

   ```bash
   make ollama
   ```

---

## ▶️ Run the Application

Start the app by running:

```bash
python app.py
```

---