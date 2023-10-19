# -*- coding: utf-8 -*-

"""
search_helper.gui_main

Main GUI

Copyright (C) 2020-2023 Rainer Schwarzbach

This file is part of search_helper.

search_helper is free software:
you can redistribute it and/or modify it under the terms of the MIT License.

search_helper is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import gettext
import os
import pathlib
import re
import sys
import textwrap
import time
import urllib.parse
import webbrowser

import tkinter

from tkinter import filedialog
from tkinter import messagebox

from typing import Any, Dict

from serializable_trees import Tree
from serializable_trees.basics import MapNode

from search_helper import __version__
from search_helper import gui_commons
from search_helper import paths


#
# Constants
#


SCRIPT_NAME = "Search Helper"
PYPI_URL = "https://pypi.org/project/search-helper/"
REPO_URL = "https://gitlab.com/blackstream-x/search-helper"
DOCS_URL = "https://blackstream-x.gitlab.io/search-helper/"
DEFAULT_CONFIG_FILE_NAME = "docs/examples/example.yaml"


#
# Classes
#


class Configuration:

    """Configuration data object for this script"""

    k_format = "Number Format"
    k_must_match = "Search Term Must Match"
    k_mutex_categories = "Mutually Exclusive Categories"
    k_regex_description = "Regex Description"
    k_register_browsers = "Register Browsers"
    k_search_urls = "Search URLs"
    k_single_url = "URL"
    k_special_keys = "Special Select Keys"
    k_urls = "URLs"

    def __init__(
        self,
        mapping: MapNode,
        config_file_name=None,
        translations=gettext.gettext,
    ):
        """Keep the data structure form the input file"""
        self._ = translations
        self.search_urls = mapping[self.k_search_urls]
        description = mapping.get("Description", "")
        if "{url_count_per_category}" in description:
            url_count_per_category = "".join(
                f"{category}: {self.get_count(category)}\n"
                for category in self.search_urls
            )
            description = description.format(
                url_count_per_category=url_count_per_category
            )
        #
        self.options = mapping.get("Options", {})
        # self.translations = mapping.get("Translations", {})
        self.special_select = {}
        if not self.options.get(self.k_mutex_categories, False):
            special_select = self.options.get(self.k_special_keys, {})
            for key, value in special_select.items():
                if key[-2] == "-":
                    access_key = f"<{key}>"
                    self.special_select[access_key] = [
                        category
                        for category in value["Categories"]
                        if category in self.search_urls
                    ]
                #
            #
        #
        self.application = MapNode(
            description=description,
            title=mapping.get("Application Title", SCRIPT_NAME),
            metadata=mapping.get("Metadata", MapNode()),
            config_file_name=config_file_name,
        )
        self.deviant_homepages = mapping.get("Deviant Homepages", MapNode())
        self.register_browsers()

    @classmethod
    def from_file(cls, config_file_name, translations):
        """Read data from a configuration file"""
        return cls(
            Tree.from_file(config_file_name).root,
            config_file_name=config_file_name,
            translations=translations,
        )

    def get_category_search_urls(self, category):
        """Return the search URLs dict for the specified category"""
        try:
            return self.search_urls[category][self.k_urls]
        except KeyError:
            return {category: self.search_urls[category][self.k_single_url]}
        #

    def get_items(self, category):
        """Return a list of (name, url) tuples
        in the specified category
        """
        category_urls = self.get_category_search_urls(category)
        return list(category_urls.items())

    def get_list_for(self, category, search_term=None):
        """Return a list of (name, URL) tuples.
        If a keyword was given, return search URLs for that keyword.
        Else, return the homepages.
        """
        if search_term:
            number_format = self.search_urls[category].get(self.k_format)
            if number_format:
                search_term = format(int(search_term), number_format)
            else:
                must_match = self.search_urls[category].get(self.k_must_match)
                try:
                    match = re.match(must_match, search_term)
                except re.error as regex_error:
                    error_location = " \u2192 ".join(
                        (self.k_search_urls, category, self.k_must_match)
                    )
                    raise ValueError(
                        self._(
                            "Error in regular expression\n"
                            "(%s)\n"
                            "Please fix the error in the file %s\n"
                            "(%s) and restart this program!"
                        )
                        % (
                            regex_error,
                            self.application.config_file_name,
                            error_location,
                        )
                    ) from regex_error
                except TypeError:
                    # No regular expression.
                    ...
                else:
                    if not match:
                        raise ValueError(
                            self._(
                                "Search term %r does not match"
                                " the regular expression %r\n(%s)\n"
                                "and will be ignored."
                            )
                            % (
                                search_term,
                                must_match,
                                self.search_urls[category].get(
                                    self.k_regex_description,
                                    self._("missing description"),
                                ),
                            )
                        )
                    #
                #
            #
            quoted_search_term = urllib.parse.quote_plus(search_term)
        else:
            quoted_search_term = None
        #
        urls_list = []
        for name, url in self.get_items(category):
            if quoted_search_term:
                url = url.format(search_term=quoted_search_term)
            else:
                try:
                    url = self.deviant_homepages[name]
                except KeyError:
                    # derive the homepage from the search URL
                    url_parts = urllib.parse.urlsplit(url)
                    url = urllib.parse.urlunsplit(url_parts[:2] + 3 * ("",))
                #
            #
            urls_list.append((name, url))
        #
        return urls_list

    def get_count(self, category):
        """Return the count of URLs per category"""
        return len(self.get_items(category))

    def register_browsers(self):
        """Register browsers defined in the config file
        if the name ist not yet occupied
        and if the path is really a file
        """
        webbrowser.get()
        try:
            browser_items = self.options[self.k_register_browsers].items()
        except (AttributeError, KeyError):
            return
        #
        for name, executable_path in browser_items:
            try:
                webbrowser.get(name)
            except webbrowser.Error:
                expanded_path = os.path.expandvars(executable_path)
                if os.path.isfile(expanded_path):
                    webbrowser.register(
                        name,
                        None,
                        webbrowser.BackgroundBrowser(expanded_path),
                    )
                #
            #
        #


# pylint: disable=too-many-instance-attributes


class UserInterface:

    """GUI using tkinter"""

    def __init__(self, config_file_name: str, *languages: str) -> None:
        """Initialize the url config and build the GUI"""
        # ------------------------------------------------------------------
        # Translation code adapted from
        # <https://codeberg.org/blackstream-x/postleid>
        translation = gettext.translation(
            "gui_main",
            localedir=paths.PACKAGE_LOCALE_PATH,
            languages=list(languages),
            fallback=True,
        )
        self._ = translation.gettext
        # self.ngettext = translation.ngettext
        # ------------------------------------------------------------------

        if config_file_name.startswith("example:"):
            config_stub = config_file_name.split(":", 1)[-1]
            config_file_path = (
                paths.PACKAGE_DATA_PATH / f"{config_stub}.shc.yaml"
            )
            if config_file_path.is_file():
                config_file_name = str(config_file_path)
            else:
                config_file_name = ""
            #
        #
        self.main_window = tkinter.Tk()
        self.config = self.__config_from_file(config_file_name)
        self.main_window.title(self.config.application.title)
        description_text = "\n".join(
            "\n".join(textwrap.wrap(paragraph, width=80))
            for paragraph in self.config.application.description.splitlines()
        )
        description_frame = tkinter.Frame(
            self.main_window,
            borderwidth=2,
            padx=5,
            pady=5,
            relief=tkinter.GROOVE,
        )
        description = tkinter.Label(
            description_frame, text=description_text, justify=tkinter.LEFT
        )
        description.grid(sticky=tkinter.W)
        description_frame.grid(padx=4, pady=2, sticky=tkinter.E + tkinter.W)
        #
        self.search_term_entry: tkinter.Entry = tkinter.Entry()
        self.categories: Dict[str, Any] = {}
        self.selectors: Dict[str, Any] = {}
        self.selected_category = tkinter.StringVar()
        self.use_radiobuttons = self.config.options.get(
            self.config.k_mutex_categories, False
        )
        self.__build_action_frame()
        for access_key, action in (
            ("<Control-d>", self.clear_search_term),
            ("<Control-x>", self.cut_search_term),
            ("<Return>", self.open_urls),
            ("<Escape>", self.quit),
        ):
            if access_key not in self.config.special_select:
                self.main_window.bind_all(access_key, action)
            #
        #
        self.search_term_entry.focus_set()
        self.main_window.mainloop()

    def __config_from_file(self, config_file_name):
        """Return a Configuration() instance from the file."""
        supported_file_types = [
            (
                self._("Search Helper Configurations"),
                (".shc.json", ".shc.yaml"),
            ),
            (self._("JSON or YAML files"), (".json", ".yaml")),
        ]
        while True:
            if config_file_name:
                return Configuration.from_file(config_file_name, self._)
            #
            config_file_name = filedialog.askopenfilename(
                title=self._("Select configuration file"),
                parent=self.main_window,
                filetypes=supported_file_types,
                initialdir=os.getcwd(),
            )
            if not config_file_name:
                self.quit()
                sys.exit(0)
            #
        #

    def __build_action_frame(self):
        """Build the action frame
        with the category selector checkbuttons or radiobuttons,
        depending on the setting of the "Mutually Exclusive Categories" option.
        Return the number of lines
        """
        # pylint: disable=too-many-branches
        action_frame = tkinter.Frame(
            self.main_window, borderwidth=2, relief=tkinter.GROOVE
        )
        search_term_label = tkinter.Label(
            action_frame, text=self._("Search Term:")
        )
        search_term_label.grid(row=0, column=0, sticky=tkinter.W)
        self.search_term_entry = tkinter.Entry(action_frame, width=50)
        self.search_term_entry.grid(
            row=0, column=1, columnspan=2, sticky=tkinter.W, padx=5, pady=5
        )
        button = tkinter.Button(
            action_frame,
            text=self._("Clear"),
            command=self.clear_search_term,
        )
        button.grid(row=0, column=3, sticky=tkinter.W)
        current_grid_row = 1
        for current_category, settings in self.config.search_urls.items():
            preferred_browser = settings.get("Preferred Browser")
            category_label = current_category
            if preferred_browser:
                try:
                    webbrowser.get(preferred_browser)
                except webbrowser.Error:
                    ...
                else:
                    category_label = self._("%s (opened in %s)") % (
                        current_category,
                        preferred_browser.title(),
                    )
                #            #
            if current_grid_row <= 12:
                access_key = f"<KeyPress-F{current_grid_row}>"
                category_label = f"{category_label} <F{current_grid_row}>"
            else:
                access_key = None
            #
            if self.use_radiobuttons:
                self.selectors[current_category] = tkinter.Radiobutton(
                    action_frame,
                    text=category_label,
                    justify=tkinter.LEFT,
                    value=current_category,
                    variable=self.selected_category,
                )
                if current_grid_row == 1:
                    self.selectors[current_category].select()
                #
            else:
                self.categories[current_category] = tkinter.IntVar()
                self.selectors[current_category] = tkinter.Checkbutton(
                    action_frame,
                    text=category_label,
                    justify=tkinter.LEFT,
                    variable=self.categories[current_category],
                )
            #
            self.selectors[current_category].grid(
                row=current_grid_row, column=0, columnspan=2, sticky=tkinter.W
            )
            if self.config.get_count(current_category) > 1:

                def show_list_handler(self=self, category=current_category):
                    """Internal function definition to process the category
                    in the "real" handler function self.show_urls_in(),
                    compare <https://tkdocs.com/shipman/extra-args.html>.
                    """
                    return self.show_urls_in(category)

                #
                button = tkinter.Button(
                    action_frame,
                    text=self._("List URLs"),
                    command=show_list_handler,
                )
                button.grid(row=current_grid_row, column=2, sticky=tkinter.W)
            else:

                def copy_url_handler(self=self, category=current_category):
                    """Internal function definition to process the category
                    in the "real" handler function self.copy_url(),
                    compare <https://tkdocs.com/shipman/extra-args.html>.
                    """
                    return self.copy_url(category)

                #
                button = tkinter.Button(
                    action_frame,
                    text=self._("Copy URL"),
                    command=copy_url_handler,
                )
                button.grid(row=current_grid_row, column=2, sticky=tkinter.W)
            #
            current_grid_row += 1
            if access_key:

                def handler(event, self=self, category=current_category):
                    """Internal function definition to process the category
                    in the "real" handler function self.__toggle_checkbox(),
                    compare <https://tkdocs.com/shipman/extra-args.html>.
                    """
                    del event
                    return self.__toggle_selector(category)

                #
                self.main_window.bind_all(access_key, handler)
            #
        #
        button = tkinter.Button(
            action_frame,
            text=self._("Start search(es)"),
            command=self.open_urls,
            default=tkinter.ACTIVE,
        )
        button.grid(
            row=current_grid_row, column=0, sticky=tkinter.W, padx=5, pady=5
        )
        button = tkinter.Button(
            action_frame,
            text=self._("About…"),
            command=self.show_about,
        )
        button.grid(
            row=current_grid_row, column=1, sticky=tkinter.W, padx=5, pady=5
        )
        button = tkinter.Button(
            action_frame,
            text=self._("Quit"),
            command=self.quit,
        )
        button.grid(
            row=current_grid_row, column=3, sticky=tkinter.E, padx=5, pady=5
        )
        #
        action_frame.grid(padx=4, pady=2, sticky=tkinter.E + tkinter.W)
        #
        for special_select_key in self.config.special_select:

            def special_handler(event, self=self, key=special_select_key):
                """Internal function definition to process the key name
                in the "real" handler function self.__select_categories(),
                compare <https://tkdocs.com/shipman/extra-args.html>.
                """
                del event
                return self.__select_categories(key)

            #
            self.main_window.bind_all(special_select_key, special_handler)
        #

    def __toggle_selector(self, category):
        """Toggle a checkbox or activate a radiobutton"""
        try:
            self.selectors[category].toggle()
        except AttributeError:
            self.selectors[category].invoke()
        #

    def __select_categories(self, special_select_key):
        """Select all categories defined in the config for the
        special select key
        """
        for category in self.config.special_select.get(special_select_key, []):
            self.categories[category].set(1)
        #

    def show_about(self):
        """Show information about the application and the source file
        in a modal dialog
        """
        license_text = self._(
            "Licensed under the MIT license, see repository."
        )
        config_file_path = pathlib.Path(
            self.config.application.config_file_name
        ).resolve()
        try:
            config_file_path.relative_to(paths.PACKAGE_DATA_PATH.resolve())
        except ValueError:
            metadata = "\n".join(
                f"{key}: {value}"
                for (key, value) in self.config.application.metadata.items()
            )
        else:
            metadata = self._("(part of the package)")
        #
        gui_commons.InfoDialog(
            self.main_window,
            gui_commons.Section(
                self._("Program"),
                gui_commons.TextBlock(f"{SCRIPT_NAME} {__version__}"),
                gui_commons.Link(PYPI_URL, label=self._("Package:")),
                gui_commons.Link(REPO_URL, label=self._("Source Repository:")),
                gui_commons.Link(DOCS_URL, label=self._("Documentation:")),
                gui_commons.TextBlock(license_text),
            ),
            gui_commons.Section(
                self._("Config File"),
                gui_commons.TextBlock(f"{config_file_path.name}\n{metadata}"),
            ),
            title=self._("About…"),
        )
        #

    def show_urls_in(self, category):
        """Show all URL names of the selected category in a modal dialog"""
        search_term = self.search_term_entry.get().strip()
        try:
            urls_list = self.config.get_list_for(
                category, search_term=search_term
            )
        except ValueError as value_error:
            messagebox.showerror(
                self._("Error for category %r") % category,
                str(value_error),
                icon=messagebox.ERROR,
            )
        else:
            links = [
                gui_commons.Link(url, label=f"{name}:")
                for (name, url) in urls_list
            ]
            gui_commons.InfoDialog(
                self.main_window,
                gui_commons.Section(category, *links),
                title=self._("List URLs"),
            )
        #

    def copy_url(self, category):
        """Copy the URL from the current text into the clipboard"""
        search_term = self.search_term_entry.get().strip()
        try:
            urls_list = self.config.get_list_for(
                category, search_term=search_term
            )
        except ValueError as value_error:
            messagebox.showerror(
                self._("Error for category %r") % category,
                str(value_error),
                icon=messagebox.ERROR,
            )
        else:
            if len(urls_list) == 1:
                self.main_window.clipboard_clear()
                self.main_window.clipboard_append(urls_list[0][1])
            #
        #

    def clear_search_term(self, event=None):
        """clear the search term entry"""
        del event
        self.search_term_entry.delete(0, tkinter.END)

    def cut_search_term(self, event=None):
        """Cut out the search term: copy it to the clipboard
        and clear the entry
        """
        del event
        search_term = self.search_term_entry.get().strip()
        if search_term:
            self.main_window.clipboard_clear()
            self.main_window.clipboard_append(search_term)
            self.clear_search_term()
        #

    def open_urls(self, event=None):
        """Open the URLs with the search keywords"""
        del event
        search_term = self.search_term_entry.get().strip()
        if self.use_radiobuttons:
            selected_categories = [self.selected_category.get()]
        else:
            selected_categories = [
                category
                for category in self.config.search_urls
                if self.categories[category].get()
            ]
        #
        for current_category in selected_categories:
            try:
                urls_list = self.config.get_list_for(
                    current_category, search_term=search_term
                )
            except ValueError as value_error:
                messagebox.showerror(
                    self._("Error for category %r") % current_category,
                    str(value_error),
                    icon=messagebox.ERROR,
                )
                continue
            #
            if not urls_list:
                continue
            #
            # Get a runnable browser instance – either the specified preferred
            # browser (if installed) or the default.
            try:
                current_browser = webbrowser.get(
                    self.config.search_urls[current_category].get(
                        "Preferred Browser"
                    )
                )
            except (webbrowser.Error, TypeError):
                current_browser = webbrowser.get()
            #
            current_browser.open_new(urls_list[0][1])
            if len(urls_list) > 1:
                time.sleep(0.5)
                for current_url in urls_list[1:]:
                    current_browser.open_new_tab(current_url[1])
                #
            #
            time.sleep(1)
        #

    def quit(self, event=None):
        """Exit the application"""
        del event
        self.main_window.destroy()


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
