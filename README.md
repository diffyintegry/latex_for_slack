LaTeX-python-bot for Slack
=============

## Overview
This is a bot by [Nick](mailto:nicholas.comment+latexbot@gmail.com) designed to work with BeepBoop.  Could be hosted elsewhere, as well, but edits to the ImgurClient sections will be necessary.  

In order for this to run, you'll need an imgur client ID and imgur secret.  These can be obtained [here](https://api.imgur.com/oauth2/addclient); you'll only need Anonymous usage.
 
If you have any questions, please send them to [Nick](mailto:nicholas.comment+latexbot@gmail.com)

Visit [Beep Boop](https://beepboophq.com/docs/article/overview) to get the scoop on the the Beep Boop hosting platform. The Slack API documentation can be found [here](https://api.slack.com/).

## Assumptions
* You have already signed up with [Beep Boop](https://beepboophq.com) and have a local fork of this project.
* If this isn't the case, contact [Nick](mailto:nicholas.comment+latexbot@gmail.com), and he can help set up the hosting.
* You have sufficient rights in your Slack team to configure a bot and generate/access a Slack API token.

## Usage

### Run locally
Install dependencies ([virtualenv](http://virtualenv.readthedocs.org/en/latest/) is recommended.)

	pip install -r requirements.txt
	export SLACK_TOKEN=<YOUR SLACK TOKEN>; python ./bot/app.py

Things are looking good if the console prints something like:

	Connected <your bot name> to <your slack team> team at https://<your slack team>.slack.com.

If you want change the logging level, prepend `export LOG_LEVEL=<your level>; ` to the `python ./bot/app.py` command.

### Run in BeepBoop
If you have linked your local repo with the Beep Boop service (check [here](https://beepboophq.com/0_o/my-projects)), changes pushed to the remote master branch will automatically deploy.

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
