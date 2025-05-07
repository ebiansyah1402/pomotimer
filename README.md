## Setting up Google Cloud Credentials

To use the Google Tasks and Calendar integration features of this Pomodoro script, you'll need to create and download your own `credentials.json` file from the Google Cloud Console. Here's how:

1.  **Go to the Google Cloud Console:**
    Open your web browser and navigate to [https://console.cloud.google.com/](https://console.cloud.google.com/).

2.  **Create a Google Cloud Project (if you don't have one):**
    * If you don't have an existing project, click on the project dropdown at the top of the page (it might say "No organization" or the name of a previous project).
    * Click on "New Project."
    * Give your project a name (e.g., "Pomodoro App Credentials") and click "Create."
    * Once the project is created, make sure it's selected in the project dropdown.

3.  **Enable the Google Tasks API and Google Calendar API:**
    * In the Google Cloud Console, navigate to **APIs & Services** > **Library** from the left-hand menu.
    * **Enable Google Tasks API:** Search for "Google Tasks API" and click on the result. If it's not enabled, click the **Enable** button.
    * **Enable Google Calendar API:** Go back to **APIs & Services** > **Library**. Search for "Google Calendar API" and click on the result. If it's not enabled, click the **Enable** button.

4.  **Configure the OAuth Consent Screen:**
    * Navigate to **APIs & Services** > **OAuth consent screen** from the left-hand menu.
    * Choose **External** as the "User type" and click **Create**.
    * Fill in the "App name" (e.g., "Pomodoro Script").
    * Select your email address in the "User support email" dropdown.
    * Scroll down to "Developer contact information" and enter your email address.
    * Click **Save and Continue** (you can skip the "Scopes" and "Optional info" for this basic use).
    * Click **Back to Dashboard**.

5.  **Create OAuth 2.0 Credentials:**
    * Navigate to **APIs & Services** > **Credentials** from the left-hand menu.
    * Click on the **+ Create credentials** button at the top.
    * Select **OAuth client ID**.
    * Choose **Desktop application** as the "Application type."
    * Give your client ID a name (e.g., "Pomodoro Desktop Client") and click **Create**.

6.  **Download the `credentials.json` file:**
    * A pop-up will appear with your "Client ID" and "Client secret." Click the **Download JSON** button.
    * **Save this downloaded file as `credentials.json` in the same directory where your `google_integration.py` script is located.**

7.  **Run `google_integration.py`:**
    * Open your terminal or command prompt, navigate to the directory containing your scripts, and run:
        ```bash
        python google_integration.py
        ```
    * The first time you run it, it will likely open a web browser asking you to authorize the application to access your Google Tasks and Calendar. Grant the necessary permissions.
    * Upon successful authorization, a `token.json` file will be created in the same directory. This file stores your access and refresh tokens.

**Important Security Notes:**

* **Keep `credentials.json` private:** Do not share this file or upload it to public repositories like GitHub.
* **Do not commit `credentials.json` or `token.json` to your Git repository.** Make sure these files are listed in your `.gitignore` file.

By following these steps, others will be able to set up their own Google Cloud credentials and use the Google integration features of your Pomodoro script.