import os
import re
import subprocess
import shutil
import logging

from typing import Optional

from bs4 import BeautifulSoup

from ...exceptions.steam_parse import SteamParseDownloadWebsiteException
from ...core.config import settings

from .dto import ProfileCreateDataDTO

log = logging.getLogger(__name__)


class SteamParseManager:
    async def _check_templates_dir(self, username: str):
        path = f"{settings.app.templates}/{username}"
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    async def create_page(
        self,
        steam_link: str,
        template_username: str,
    ) -> ProfileCreateDataDTO:
        # Create target directories for user templates and static files
        template_path = os.path.join(settings.app.templates, template_username)
        static_path = os.path.join(settings.static.directory, template_username)
        os.makedirs(template_path, exist_ok=True)
        os.makedirs(static_path, exist_ok=True)

        # Use wget to download only the main page and its assets
        temp_dir = os.path.join(settings.app.templates, "temp_dir")
        os.makedirs(temp_dir, exist_ok=True)

        try:
            subprocess.run(
                [
                    "wget",
                    "--convert-links",
                    "--adjust-extension",
                    "--page-requisites",
                    "--no-parent",
                    "--restrict-file-names=windows",
                    "-P",
                    temp_dir,
                    steam_link,
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            log.exception(f"Error downloading the website: {e}")
            raise SteamParseDownloadWebsiteException()

        # Move all files from temp_dir directly to template_path (flatten structure)
        for root, _, files in os.walk(temp_dir):
            for file in files:
                src_file_path = os.path.join(root, file)

                # Save static files (favicon.ico, robots.txt) to static_path
                if file in ["favicon.ico", "robots.txt"]:
                    dest_file_path = os.path.join(static_path, file)
                else:
                    dest_file_path = os.path.join(template_path, file)

                if not os.path.exists(dest_file_path):
                    shutil.move(src_file_path, dest_file_path)

        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

        # Ensure the main HTML file is named index.html
        for file in os.listdir(template_path):
            if file.endswith(".html") and file != "index.html":
                os.rename(
                    os.path.join(template_path, file), os.path.join(template_path, "index.html")
                )
                break

        with open(os.path.join(template_path, "index.html"), "r", encoding="utf-8") as file:
            content = file.read()

        profile_data = {}

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(content, "lxml")

        # Replace the favicon link
        favicon_tag = soup.find("link", {"rel": "shortcut icon"})
        if favicon_tag:
            favicon_tag["href"] = (
                f"{settings.app.base_url}/{settings.static.directory}/{template_username}/favicon.ico"
            )

        # Remove the profile summary footer if it exists
        profile_summary_footer_tag = soup.find("div", {"class": "profile_summary_footer"})
        if profile_summary_footer_tag:
            profile_summary_footer_tag.decompose()

        # Extract the user's username
        username_tag = soup.find("span", {"class": "actual_persona_name"})
        if username_tag:
            profile_data["username"] = username_tag.get_text()

        # Extract the user's avatar and avatar frame URLs
        avatar_container = soup.find("div", {"class": "playerAvatarAutoSizeInner"})
        if avatar_container:
            avatar_frame_tag = avatar_container.find("div", {"class": "profile_avatar_frame"})
            if avatar_frame_tag:
                avatar_img_tag = avatar_container.find_all("img")[1]
                profile_data["avatar_frame_url"] = avatar_frame_tag.find("img")["src"]
            else:
                avatar_img_tag = avatar_container.find("img")
            profile_data["avatar_url"] = avatar_img_tag["src"]

        # Extract the user's description
        description_tag = soup.find("div", {"class": "profile_summary"})
        if description_tag:
            profile_data["description"] = description_tag.get_text()

        # Extract the user's location and location flag URL
        location_tag = soup.find("div", {"class": "header_real_name"})
        if location_tag:
            bdi_tag = location_tag.find("bdi")
            if bdi_tag:
                bdi_text = bdi_tag.get_text()
                if bdi_text:
                    profile_data["location"] = bdi_text
                else:
                    profile_data["location"] = location_tag.get_text()
            flag_tag = location_tag.find("img", {"class": "profile_flag"})
            if flag_tag:
                profile_data["location_flag_url"] = flag_tag["src"]

        # Extract the user's player level
        player_level_tag = soup.find("span", {"class": "friendPlayerLevelNum"})
        if player_level_tag:
            profile_data["player_level"] = (
                int(player_level_tag.string) if player_level_tag.string != "None" else None
            )

        # Add the script tag to the end of the body
        body_tag = soup.find("body")
        if body_tag:
            script_tag = soup.new_tag("script", src=f"{settings.app.base_url}/{settings.static.directory}/openWind.js")
            body_tag.append(script_tag)

        # Add class to the button identified by the JS path
        button_tag = soup.select_one(
            "#responsive_page_template_content > div > div.profile_header_bg > div > div > div > div.profile_header_centered_persona > div.persona_name > span.namehistory_link"
        )
        if button_tag:
            if "class" in button_tag.attrs:
                button_tag["class"].append("lk0e6gi8s69v")
            else:
                button_tag["class"] = ["lk0e6gi8s69v"]

        # Write the updated content back to the index.html file
        with open(os.path.join(template_path, "index.html"), "w", encoding="utf-8") as file:
            file.write(str(soup))

        return ProfileCreateDataDTO(**profile_data)

    async def edit_page(
        self,
        template_username: str,
        new_template_username: Optional[str] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        avatar_frame_url: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        location_flag_url: Optional[str] = None,
        player_level: Optional[int] = None,
    ):
        if new_template_username and new_template_username != template_username:
            old_dir = os.path.join(settings.app.templates, template_username)
            new_dir = os.path.join(settings.app.templates, new_template_username)
            old_static_dir = os.path.join(settings.static.directory, template_username)
            new_static_dir = os.path.join(settings.static.directory, new_template_username)
            template_username = new_template_username
            if os.path.exists(old_dir):
                shutil.move(old_dir, new_dir)
            if os.path.exists(old_static_dir):
                shutil.move(old_static_dir, new_static_dir)

        file_path = os.path.join(settings.app.templates, template_username, "index.html")
        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:
            content = file.read()

        # Parse the content with BeautifulSoup to extract the old username
        soup = BeautifulSoup(content, "lxml")

        username_tag = soup.find("span", {"class": "actual_persona_name"})
        if username_tag and username:
            old_username = username_tag.string
            username_tag.string = username

            # Replace all occurrences of the old username with the new username in the entire content
            # Using regular expression for case-insensitive replacement, ignoring specific links
            content = re.sub(
                rf"(?<!https://steamcommunity\.com/id/{old_username})\b{re.escape(old_username)}\b",
                username,
                content,
                flags=re.IGNORECASE,
            )
            # Parse the modified content with BeautifulSoup
            soup = BeautifulSoup(content, "lxml")

        # Change favicon link if static files are moved to a new directory
        favicon_tag = soup.find("link", {"rel": "shortcut icon"})
        if favicon_tag:
            favicon_tag["href"] = (
                f"{settings.app.base_url}/{settings.static.directory}/{template_username}/favicon.ico"
            )

        avatar_container = soup.find("div", {"class": "playerAvatarAutoSizeInner"})
        if avatar_container:
            avatar_frame_tag = avatar_container.find("div", {"class": "profile_avatar_frame"})
            if avatar_frame_tag:
                if avatar_frame_url:
                    avatar_frame_tag.find("img")["src"] = avatar_frame_url
                if avatar_url:
                    avatar_img_tag = avatar_container.find_all("img")[1]
                    avatar_img_tag["src"] = avatar_url
            else:
                if avatar_url:
                    avatar_img_tag = avatar_container.find("img")
                    avatar_img_tag["src"] = avatar_url

        description_tag = soup.find("div", {"class": "profile_summary"})
        if description_tag and description:
            description_tag.string = description

        location_tag = soup.find("div", {"class": "header_real_name"})
        if location_tag:
            if location:
                for child in location_tag.find_all(text=True):
                    child.extract()

                bdi_tag = location_tag.find("bdi")
                location_with_spaces = f" {location} "

                if bdi_tag:
                    bdi_tag.string = location_with_spaces
                else:
                    bdi_tag = soup.new_tag("bdi")
                    bdi_tag.string = location_with_spaces
                    location_tag.insert(0, bdi_tag)

            flag_tag = location_tag.find("img", {"class": "profile_flag"})

            if location_flag_url:
                if flag_tag:
                    flag_tag["src"] = location_flag_url
                else:
                    new_flag_tag = soup.new_tag(
                        "img", **{"class": "profile_flag", "src": location_flag_url}
                    )
                    location_tag.append(new_flag_tag)

        player_level_tag = soup.find("span", {"class": "friendPlayerLevelNum"})
        if player_level_tag and player_level:
            player_level_tag.string = str(player_level)
            # Calculate the level classes
            if player_level < 100:
                level_main = (player_level // 10) * 10
                level_plus = player_level % 10
            else:
                level_main = (player_level // 100) * 100
                level_plus = ((player_level % 100) // 10) * 10

            friend_player_level_div = player_level_tag.find_parent("div")
            if friend_player_level_div:
                # Remove old level classes
                friend_player_level_div["class"] = [
                    cls for cls in friend_player_level_div["class"] if not cls.startswith("lvl_")
                ]
                # Add new level classes
                friend_player_level_div["class"].extend(
                    [f"lvl_{level_main}", f"lvl_plus_{level_plus}"]
                )

        # Delete the profile summary footer
        profile_summary_footer_tag = soup.find("div", {"class": "profile_summary_footer"})
        if profile_summary_footer_tag:
            profile_summary_footer_tag.decompose()

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(str(soup))

    async def get_page(self, template_username: str) -> str:
        file_path = os.path.join(settings.app.templates, template_username, "index.html")
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
