<p align="center">
  <img src="resources/logo/logo-circle.png" width="200">
</p>

# 🎉 What is this?
<p align="center">
  <img src="https://github.com/user-attachments/assets/8a85a9f0-8996-4956-862f-0c4387dba491" width="300" height="400">
</p>

I don't like the official website, I don't like visiting there every day to see just the menu. Here, Hacettepe Cafeteria
Bot comes as a simple solution to this issue. What's even better is that you don't need to install mobile or desktop
apps to use such a simple tool. You can directly use it via Telegram.

| **Platform**            | **Description**                                    | **Link**                                                                                    |
|-------------------------|----------------------------------------------------|---------------------------------------------------------------------------------------------|
| **🤖 Telegram Bot**     | Directly interact with the Hacettepe Cafeteria Bot | [🌐](https://t.me/HacettepeYemekhaneciBot)                                                  |
| **📢 Telegram Channel** | Get the updates with image only                    | [🌐](https://t.me/hacettepeyemekhane)                                                       |
| **📢 Telegram Channel** | Get the updates with text only                     | [🌐](https://t.me/hacettepeyemekhaneText)                                                   |
| **📧 Mailing List**     | Subscribe to receive updates via email             | [🌐](mailto:hacettepe-cafetaria-list+subscribe@ozguryazilimhacettepe.com?subject=Subscribe) |

# 🦾 How To Contribute?
Hacettepe Cafeteria Bot is an uncomplicated tool with a straightforward aim. Only thing that makes it really useful is the
problem it solves. Therefore, we don't see many contributions. Yet, you can still request new features or report the
issues you faced. For those who knows a bit Python also can help with the development.

## 🐛 Feature Requests & Reporting Issues
Any *"I encountered this bug or that bug"* or *"oh, I think this feature would be useful"* type of communications can be
done by opening an issue on GitHub. If you don't use GitHub, and came here to see what's going on, you can send email to
current maintainer [furkansimsekli](mailto:simseklifurkan0@gmail.com).

## 💻 Development
Grab an issue from the list, and open a PR. Issues with `good first issue` tags are specifically tagged that way so that
new volunteers can make contributions easier. Please consider opening a new issue if you are going to do something
*unheard* of.

### 🏠 Development Environment
After cloning the repository, you should create a virtual environment. Python3.11 is recommended but any version higher
than or equal to 3.9 should work just fine. Then, install the requirements.

```bash
# Clone the repository
git clone git@github.com:hacettepeoyt/hu-cafeteria-bot.git
cd hu-cafeteria-bot

# Create a virtual environment with venv and activate it 
python3 -m venv .venv
source .venv/bin/activate

# Install the requirements
pip install -r requirements.txt
```

Fill the missing configurations in `config.toml`. Then, run the following command:

```bash
python -m src -c <path/to/config.toml> -d <path/to/database.json>
```

# 📃 License
[GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
