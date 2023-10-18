import re
from pathlib import Path

import astropy.units as u
import customtkinter as ctk
import matplotlib as mpl
import numpy as np
import tomlkit
from astropy.coordinates import SkyCoord
from astropy.table import QTable
from CTkMessagebox import CTkMessagebox
from tqdm import tqdm

from pygcg.tabs.beams import BeamFrame
from pygcg.tabs.spectrum import SpecFrame
from pygcg.windows.comments import CommentsWindow
from pygcg.windows.settings import SettingsWindow
from pygcg.utils.misc import fpe, flatten_dict


class GCG(ctk.CTk):
    def __init__(self, config_file=None):
        super().__init__()

        # Geometry
        self.geometry("1366x768")
        self.minsize(1280, 720)
        # self.attributes("-zoomed", True)
        self.title("GLASS-JWST Classification GUI")

        self.initialise_configuration(config_file)
        self.settings_window = None
        self.comments_window = None

        # Key bindings
        self.protocol(
            "WM_DELETE_WINDOW",
            self.quit_gracefully,
        )

        self.bind("<Control-q>", self.quit_gracefully)
        self.bind("<Left>", self.prev_gal_button_callback)
        self.bind("<Right>", self.next_gal_button_callback)
        self.bind("<c>", self.gal_comments_button_callback)

        # configure grid system
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Setup bottom navigation buttons
        nav_frame = ctk.CTkFrame(self)
        nav_frame.grid(
            column=0,
            row=2,
            # columnspan=5,
            sticky="ew",
        )
        nav_frame.grid_columnconfigure((0, 1, 3, 5, 6, 7), weight=1, uniform="blah")
        nav_frame.grid_columnconfigure((2, 4), weight=0, uniform="other")

        self.read_write_button = ctk.CTkSegmentedButton(
            nav_frame,
            values=["Read-only", "Write output"],
            selected_color="red",
            selected_hover_color="dark red",
            command=self.read_write_colour,
        )
        self.read_write_button.grid(
            row=0,
            column=1,
            padx=20,
            pady=10,
            sticky="ew",
        )
        self.read_write_button.set("Read-only")

        self.open_settings_button = ctk.CTkButton(
            nav_frame,
            text="Settings",
            command=self.open_settings_callback,
        )
        self.open_settings_button.grid(
            row=1,
            column=1,
            padx=20,
            pady=10,
            sticky="ew",
        )
        self.prev_gal_button = ctk.CTkButton(
            nav_frame,
            text="Previous",
            command=self.prev_gal_button_callback,
        )
        self.prev_gal_button.grid(
            row=0, column=0, padx=20, pady=10, rowspan=2, sticky="news"
        )
        self.next_gal_button = ctk.CTkButton(
            nav_frame,
            text="Next",
            command=self.next_gal_button_callback,
        )
        self.next_gal_button.grid(
            row=0, column=7, padx=20, pady=10, rowspan=2, sticky="news"
        )
        self.comments_button = ctk.CTkButton(
            nav_frame,
            text="Comments",
            command=self.gal_comments_button_callback,
        )
        self.comments_button.grid(
            row=0,
            column=6,
            padx=20,
            pady=10,
            sticky="ew",
        )

        self.current_gal_data = {}

        self.current_gal_id = ctk.StringVar(master=self)
        self.current_gal_coords = ctk.StringVar(master=self)
        gal_id_label = ctk.CTkLabel(
            nav_frame,
            text="Current ID:",
        )
        gal_id_label.grid(
            row=0,
            column=2,
            padx=(20, 5),
            pady=10,
            sticky="e",
        )
        gal_coord_label = ctk.CTkLabel(
            nav_frame,
            text="Location:",
        )
        gal_coord_label.grid(
            row=0,
            column=4,
            padx=(20, 5),
            pady=10,
            sticky="e",
        )
        progress_label = ctk.CTkLabel(
            nav_frame,
            text="Progress:",
        )
        progress_label.grid(
            row=1,
            column=2,
            padx=(20, 5),
            pady=10,
            sticky="e",
        )
        self.progress_status = ctk.CTkLabel(
            nav_frame,
            text="???:",
        )
        self.progress_status.grid(
            row=1,
            column=3,
            padx=(5, 20),
            pady=10,
            sticky="w",
        )
        self.current_gal_entry = ctk.CTkEntry(
            nav_frame,
            textvariable=self.current_gal_id,
        )
        self.current_gal_entry.bind(
            "<Return>",
            self.change_id_entry,
        )
        self.current_gal_entry.grid(
            row=0,
            column=3,
            padx=(5, 20),
            pady=10,
            sticky="w",
        )

        self.coord_entry = ctk.CTkEntry(
            nav_frame,
            textvariable=self.current_gal_coords,
        )
        self.coord_entry.bind(
            "<Return>",
            self.change_sky_coord,
        )
        self.coord_entry.grid(
            row=0,
            column=5,
            padx=(5, 20),
            pady=10,
            sticky="w",
        )
        self.find_coord_button = ctk.CTkButton(
            nav_frame,
            text="Sky search",
            command=self.change_sky_coord,
        )
        self.find_coord_button.grid(row=1, column=5, padx=(5, 20), pady=10, sticky="w")

        self.rescan_and_reload()

    def rescan_and_reload(self):
        try:
            # assert len(self.config["files"]["out_dir"]) > 0
            # assert len(self.config["files"]["cat_path"]) > 0
            assert len(self.config["files"]["extractions_dir"]) > 0

            try:
                self.cat = QTable.read(fpe(self.config["files"]["cat_path"]))
            except:
                try:
                    self.cat = QTable.read(
                        [*fpe(self.config["files"]["extractions_dir"]).glob("*ir.cat.fits")][0]
                    )
                except:
                    self.cat = None

            assert self.cat is not None



            self.filter_names = [
                self.config["grisms"].get("R", "F200W"),
                self.config["grisms"].get("G", "F150W"),
                self.config["grisms"].get("B", "F115W"),
            ]
            self.PAs = [
                str(self.config["grisms"].get("PA1", 72.0)),
                str(self.config["grisms"].get("PA2", 341.0)),
            ]

            try:
                assert len(self.config["files"]["out_dir"]) > 0

                fpe(self.config["files"]["out_dir"]).mkdir(exist_ok=True, parents=True)
                self.out_dir = fpe(self.config["files"]["out_dir"])

                if len(self.config["files"]["temp_dir"]) > 0:
                    fpe(self.config["files"]["temp_dir"]).mkdir(exist_ok=True, parents=True)
                    self.temp_dir = fpe(self.config["files"]["temp_dir"])
                else:
                    self.temp_dir = self.out_dir / ".temp"
                    self.temp_dir.mkdir(exist_ok=True)
                
                self.out_cat_path = (
                    fpe(self.config["files"]["out_dir"]) / "pyGCG_output.fits"
                )
                self.read_write_button.configure(state="normal")
            except:
                print("Could not find or create output directory. Disabling write mode.")
                self.read_write_button.set("Read-only")
                self.read_write_button.configure(state="disabled")

            try:
                self.out_cat = QTable.read(self.out_cat_path)
            except:
                self.out_cat = QTable(
                    names=[
                        "ID",
                        "SEG_ID",
                        "RA",
                        "DEC",
                        f"{self.filter_names[2]},{self.PAs[0]}_QUALITY",
                        f"{self.filter_names[2]},{self.PAs[0]}_COVERAGE",
                        f"{self.filter_names[1]},{self.PAs[0]}_QUALITY",
                        f"{self.filter_names[1]},{self.PAs[0]}_COVERAGE",
                        f"{self.filter_names[0]},{self.PAs[0]}_QUALITY",
                        f"{self.filter_names[0]},{self.PAs[0]}_COVERAGE",
                        f"{self.filter_names[2]},{self.PAs[1]}_QUALITY",
                        f"{self.filter_names[2]},{self.PAs[1]}_COVERAGE",
                        f"{self.filter_names[1]},{self.PAs[1]}_QUALITY",
                        f"{self.filter_names[1]},{self.PAs[1]}_COVERAGE",
                        f"{self.filter_names[0]},{self.PAs[1]}_QUALITY",
                        f"{self.filter_names[0]},{self.PAs[1]}_COVERAGE",
                        "GRIZLI_REDSHIFT",
                        "ESTIMATED_REDSHIFT",
                        "COMMENTS",
                    ],
                    dtype=[
                        str,
                        int,
                        float,
                        float,
                        str,
                        float,
                        str,
                        float,
                        str,
                        float,
                        str,
                        float,
                        str,
                        float,
                        str,
                        float,
                        float,
                        float,
                        str,
                    ],
                )

            self.id_col = self.cat[self.config["cat"].get("id", "id")].astype(str)
            self.seg_id_col = self.cat[
                self.config["cat"].get("seg_id", self.config["cat"].get("id", "id"))
            ].astype(int)

            # Segmentation map ids must be a unique identifier!
            # If you're reading this message, something has gone horribly wrong
            self.seg_id_col, unique_idx = np.unique(self.seg_id_col, return_index=True)
            self.id_col = self.id_col[unique_idx]
            self.cat = self.cat[unique_idx]
            dir_to_chk = fpe(self.config["files"]["extractions_dir"])

            id_idx_list = []

            row_ids = [s.stem[-9:-4] for s in dir_to_chk.glob("*.row.fits")]
            stack_ids = [s.stem[-11:-6] for s in dir_to_chk.glob("*.stack.fits")]
            oned_ids = [s.stem[-8:-3] for s in dir_to_chk.glob("*.1D.fits")]

            for i, (n, s) in tqdm(
                enumerate(zip(self.id_col, self.seg_id_col)),
                desc="Scanning directory for objects in catalogue",
                total=len(self.id_col),
            ):
                if self.config["files"].get("skip_existing", True):
                    if s in self.out_cat["SEG_ID"]:
                        continue
                if (
                    f"{s:0>5}" in row_ids
                    and f"{s:0>5}" in oned_ids
                    and f"{s:0>5}" in stack_ids
                ):
                    id_idx_list.append(i)
            try:
                sorted_idx = np.asarray(id_idx_list)[
                    np.argsort(self.id_col[id_idx_list].astype(float))
                ]

            except Exception as e:
                sorted_idx = id_idx_list

            self.id_col = self.id_col[sorted_idx]
            self.seg_id_col = self.seg_id_col[sorted_idx]
            self.cat = self.cat[sorted_idx]
            self.sky_coords = SkyCoord(
                self.cat[self.config["cat"].get("ra", "ra")],
                self.cat[self.config["cat"].get("dec", "dec")],
            )

            assert len(self.id_col) > 0

            self.current_gal_id.set(self.id_col[0])
            self.tab_row = self.cat[0]
            self.seg_id = self.seg_id_col[0]

            self.set_current_data()

            self.generate_tabs()
        except Exception as e:
            print(e)
            self.generate_splash()

    def generate_splash(self):
        self.splash_frame = ctk.CTkFrame(self)
        self.splash_frame.grid(row=0, column=0, rowspan=2, sticky="news")
        self.splash_frame.columnconfigure(0, weight=1)
        self.splash_frame.rowconfigure(0, weight=1)
        main_label = ctk.CTkLabel(
            self.splash_frame,
            text=(
                "No objects found. Check the supplied directories, \n"
                "or rescan the current directory in the settings menu."
            ),
            font=ctk.CTkFont(family="", size=20),
        )
        main_label.grid(row=0, column=0, sticky="news")

    def generate_tabs(self):
        if hasattr(self, "splash_frame"):
            self.splash_frame.destroy()
            del self.splash_frame

        self.plot_options = {
            "cmap": "plasma",
            "stretch": "Square root",
            "limits": "grizli default",
        }

        self.tab_names = [
            f"Orientation 1: {self.PAs[0]} deg",
            f"Orientation 2: {self.PAs[1]} deg",
            f"Spectrum",
        ]
        self.object_progress = {}
        for n in self.tab_names:
            self.object_progress[n] = False
        self.update_progress()

        self.main_tabs = MyTabView(
            master=self,
            tab_names=self.tab_names,
            command=self.main_tabs_update,
        )
        self.main_tabs.grid(row=1, column=0, padx=20, pady=0, sticky="news")
        self.main_tabs._segmented_button.grid(sticky="ew")

        self.full_spec_frame = SpecFrame(
            self.main_tabs.tab(self.tab_names[2]), self.current_gal_id.get()
        )
        self.full_spec_frame.pack(fill="both", expand=1)

        self.beam_frame_1 = BeamFrame(
            self.main_tabs.tab(self.tab_names[0]),
            self.current_gal_id.get(),
            self.PAs[0],
        )
        self.beam_frame_1.pack(fill="both", expand=1)
        self.beam_frame_2 = BeamFrame(
            self.main_tabs.tab(self.tab_names[1]),
            self.current_gal_id.get(),
            self.PAs[1],
        )
        self.beam_frame_2.pack(fill="both", expand=1)

        self.quality_key_map = np.array(
            [["q", "w", "e", "r"], ["u", "i", "o", "p"], ["a", "s", "d", "f"]]
        )
        for l in self.quality_key_map.flatten():
            self.bind(f"{l}", self.select_quality_menu)

        self.object_progress[self.main_tabs.get()] = True
        self.update_progress()

    def select_quality_menu(self, event=None):
        if self.beam_frame_1.winfo_viewable():
            widg = self.beam_frame_1
        else:
            widg = self.beam_frame_2
        widg.beam_single_PA_frame.quality_frame.keypress_select(
            event, self.quality_key_map
        )

    def initialise_configuration(self, config_file=None):
        try:
            if config_file is not None:
                self.config_file_path = fpe(config_file)
            else:
                self.config_file_path = "./config.toml"
            with open(config_file, "rt") as fp:
                self.config = tomlkit.load(fp)
            self.write_config()
        except Exception as e:
            print(e)
            print(
                "No valid config file supplied. Creating config.toml in the current working directory."
            )
            example_path = Path(__file__).parent / "example_config.toml"
            with open(example_path, "rt") as fp:
                self.config = tomlkit.load(fp)
            self.config_file_path = fpe(Path.cwd() / "config.toml")
            with open(
                self.config_file_path,
                mode="wt",
                encoding="utf-8",
            ) as fp:
                tomlkit.dump(self.config, fp)

        ctk.set_appearance_mode(self.config["appearance"]["appearance_mode"].lower())
        ctk.set_default_color_theme(self.config["appearance"]["theme"].lower())
        self.change_plot_colours()

    def change_plot_colours(self):
        if ctk.get_appearance_mode() == "Dark":
            mode = 1
        else:
            mode = 0
        self.bg_colour_name = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][mode]
        self.bg_colour = [
            a / 65535
            for a in self.winfo_rgb(
                ctk.ThemeManager.theme["CTkFrame"]["fg_color"][mode]
            )
        ]
        self.text_colour = [
            a / 65535
            for a in self.winfo_rgb(
                ctk.ThemeManager.theme["CTkLabel"]["text_color"][mode]
            )
        ]

        mpl.rcParams["text.color"] = self.text_colour
        mpl.rcParams["axes.labelcolor"] = self.text_colour
        mpl.rcParams["xtick.color"] = self.text_colour
        mpl.rcParams["ytick.color"] = self.text_colour
        mpl.rcParams["axes.edgecolor"] = self.text_colour
        mpl.rcParams["axes.facecolor"] = "white" if mode == 0 else "k"

    def write_config(self):
        try:
            files = self.config["files"]
        except:
            files_tab = tomlkit.table()
            self.config.add("files", files_tab)
            files = self.config["files"]

        for f in ["extractions_dir"]:
            try:
                files[f]
            except:
                files.add(f, "")

        # Catalogue
        try:
            cat = self.config["cat"]
        except:
            cat_tab = tomlkit.table()
            self.config.add("cat", cat_tab)

        # Grisms
        try:
            grisms = self.config["grisms"]
        except:
            grism_tab = tomlkit.table()
            self.config.add("grisms", grism_tab)

        # Appearance
        try:
            appearance = self.config["appearance"]
        except:
            appearance_tab = tomlkit.table()
            self.config.add("appearance", appearance_tab)
            appearance = self.config["appearance"]

        try:
            appearance["appearance_mode"]
        except:
            appearance.add("appearance_mode", "system")
            appearance["appearance_mode"].comment("System (default), light, or dark.")

        try:
            appearance["theme"]
        except:
            appearance.add("theme", "blue")
            appearance["theme"].comment(
                "Blue (default), dark-blue, or green. The CustomTKinter color theme. "
                + "Can also point to the location of a custom .json file describing the desired theme."
            )

        # Lines
        try:
            lines = self.config["lines"]
        except:
            lines_tab = tomlkit.table()
            lines_tab.add(
                tomlkit.comment(
                    "These tables define the lines shown in the redshift tab."
                )
            )
            lines_tab.add(tomlkit.nl())
            self.config.add(tomlkit.nl())
            self.config.add("lines", lines_tab)
            lines = self.config["lines"]

        try:
            emission = lines["emission"]
        except:
            lines.add("emission", tomlkit.table().indent(4))
            emission = lines["emission"]
            emission.add(tomlkit.comment("These are the emission lines."))
            emission.add(tomlkit.nl())

        em_lines = {
            "Lyman_alpha": {
                "latex_name": r"Ly$\alpha$",
                "centre": 1215.24,
            },
            "H_alpha": {
                "latex_name": r"H$\alpha$",
                "centre": 6564.61,
            },
        }

        for line_name, line_data in em_lines.items():
            try:
                emission[line_name]
                for key in line_data.keys():
                    emission[line_name][key]
            except:
                emission.add(line_name, tomlkit.table().indent(4))
                for key, value in line_data.items():
                    emission[line_name].add(key, value)
                emission.add(tomlkit.nl())

        try:
            absorption = lines["absorption"]
        except:
            lines.add("absorption", tomlkit.table().indent(4))
            absorption = lines["absorption"]
            absorption.add(tomlkit.comment("These are the absorption lines."))
            absorption.add(tomlkit.nl())

        with open(
            fpe(self.config_file_path),
            mode="wt",
            encoding="utf-8",
        ) as fp:
            tomlkit.dump(self.config, fp)

        return self.config

    def update_progress(self):
        num = np.sum([*self.object_progress.values()])
        blocks = num * 4 * "\u2588"
        self.progress_status.configure(text=f"|{blocks:\u2581<12}| {num}/3")

    def open_settings_callback(self, event=None):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)
        else:
            self.settings_window.focus()

    def gal_comments_button_callback(self, event=None):
        if event != None and event.widget.winfo_class() == ("Entry" or "Textbox"):
            return
        if self.comments_window is None or not self.comments_window.winfo_exists():
            self.comments_window = CommentsWindow(self)
        else:
            self.comments_window.focus()

    def prev_gal_button_callback(self, event=None):
        if event != None and event.widget.winfo_class() == ("Entry" or "Textbox"):
            return
        current_tab = self.main_tabs.get()
        if current_tab == self.tab_names[2]:
            self.main_tabs.set(self.tab_names[1])
            self.main_tabs_update()
        elif current_tab == self.tab_names[1]:
            self.main_tabs.set(self.tab_names[0])
            self.main_tabs_update()
        elif current_tab == self.tab_names[0]:
            self.save_current_object()
            current_gal_idx = (self.id_col == self.current_gal_id.get()).nonzero()[0]
            self.current_gal_id.set(
                self.id_col[(current_gal_idx - 1) % len(self.id_col)][0]
            )
            self.main_tabs.set(self.tab_names[2])
            self.change_gal_id()
        self.object_progress[self.main_tabs.get()] = True
        self.update_progress()

    def next_gal_button_callback(self, event=None):
        if event != None and event.widget.winfo_class() == ("Entry" or "Textbox"):
            return
        current_tab = self.main_tabs.get()
        if current_tab == self.tab_names[0]:
            self.main_tabs.set(self.tab_names[1])
            self.main_tabs_update()
        elif current_tab == self.tab_names[1]:
            self.main_tabs.set(self.tab_names[2])
            self.main_tabs_update()
        elif current_tab == self.tab_names[2]:
            self.save_current_object()
            current_gal_idx = (self.id_col == self.current_gal_id.get()).nonzero()[0]
            self.current_gal_id.set(
                self.id_col[(current_gal_idx + 1) % len(self.id_col)][0]
            )
            self.main_tabs.set(self.tab_names[0])
            self.change_gal_id()
        self.object_progress[self.main_tabs.get()] = True
        self.update_progress()

    def save_current_object(self, event=None):
        ### This is where the logic for loading/updating the tables will go
        flattened_data = flatten_dict(self.current_gal_data)

        if (
            len(flattened_data) == 19
            and self.read_write_button.get() == "Write output"
            and np.sum([*self.object_progress.values()]) == 3
        ):
            if flattened_data["SEG_ID"] in self.out_cat["SEG_ID"]:
                warn_overwrite = CTkMessagebox(
                    title="Object already classified!",
                    message=(
                        "The data products for this object have already been classified. "
                        "Overwrite existing classification?\n"
                        "(This operation cannot be undone.)"
                    ),
                    icon="warning",
                    option_1="Cancel",
                    option_2="Overwrite",
                    option_focus=2,
                )
                if warn_overwrite.get() == "Cancel":
                    self.focus()
                    return
                else:
                    self.out_cat.remove_rows(
                        (flattened_data["SEG_ID"] == self.out_cat["SEG_ID"]).nonzero()[
                            0
                        ]
                    )
                    self.focus()
            self.out_cat.add_row(flattened_data)
            self.out_cat.write(self.out_cat_path, overwrite=True)

    def change_gal_id(self, event=None):
        for n in self.tab_names:
            self.object_progress[n] = False
        self.update_progress()
        self.tab_row = self.cat[self.id_col == self.current_gal_id.get()]
        if len(self.tab_row) > 1:
            self.tab_row = self.tab_row[0]
        self.seg_id = self.seg_id_col[self.id_col == self.current_gal_id.get()][0]

        self.set_current_data()

        self.main_tabs_update()
        self.focus()

    def set_current_data(self):
        self.current_gal_data = {}
        self.current_gal_data["id"] = self.current_gal_id.get()
        self.current_gal_data["seg_id"] = self.seg_id
        self.current_gal_data["ra"] = self.tab_row[self.config["cat"].get("ra", "ra")]
        self.current_gal_data["dec"] = self.tab_row[
            self.config["cat"].get("dec", "dec")
        ]
        self.current_gal_data["comments"] = ""

        self.current_gal_coords.set(
            self.sky_coords[self.seg_id_col == self.seg_id].to_string(
                "decimal", precision=6
            )[0]
        )

        if self.seg_id in self.out_cat["SEG_ID"]:
            out_row = self.out_cat[self.out_cat["SEG_ID"] == self.seg_id][0]
            if not hasattr(out_row["COMMENTS"], "mask"):
                self.current_gal_data["comments"] = out_row["COMMENTS"]

            for g in self.filter_names:
                for p in self.PAs:
                    self.current_gal_data[f"{g},{p}"] = {
                        "quality": out_row[f"{g},{p}_QUALITY"]
                    }

    def change_sky_coord(self, event=None):
        new_coord = None
        try:
            new_coord = SkyCoord(self.current_gal_coords.get())
        except ValueError:
            try:
                parts = re.split("\s*[,|;|\s]\s*", self.current_gal_coords.get())
                if len(parts) == 2:
                    new_coord = SkyCoord(
                        float(parts[0]) * u.deg, float(parts[1]) * u.deg
                    )
            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print(e)
            pass

        if new_coord is None:
            error = CTkMessagebox(
                title="Error",
                message="Could not parse input as on-sky coordinates.",
                icon="cancel",
                option_focus=1,
            )
            if error.get() == "OK":
                self.focus()
                return

        sky_match_idx, dist, _ = new_coord.match_to_catalog_sky(self.sky_coords)

        print (f"Closest match: ID {self.id_col[sky_match_idx]}, on-sky distance {dist[0].to(u.arcsec)}.")

        self.current_gal_id.set(self.id_col[sky_match_idx])

        self.focus()
        self.save_current_object()
        self.change_gal_id()

    def change_id_entry(self, event=None):
        self.save_current_object()
        self.change_gal_id()

    def read_write_colour(self, event=None):
        if self.read_write_button.get() == "Read-only":
            self.read_write_button.configure(
                selected_color="red", selected_hover_color="dark red"
            )
        if self.read_write_button.get() == "Write output":
            self.read_write_button.configure(
                selected_color="green", selected_hover_color="dark green"
            )

    def main_tabs_update(self):
        self.object_progress[self.main_tabs.get()] = True
        self.update_progress()
        if self.main_tabs.get() == self.tab_names[2]:
            self.full_spec_frame.update_plot()
        if self.main_tabs.get() == self.tab_names[0]:
            self.beam_frame_1.update_grid()
        if self.main_tabs.get() == self.tab_names[1]:
            self.beam_frame_2.update_grid()

    def quit_gracefully(self, event=None):
        self.write_config()
        self.quit()


class MyTabView(ctk.CTkTabview):
    def __init__(self, master, tab_names, expose_bind_fns=None, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        for i, name in enumerate(tab_names):
            self.add(name)
            try:
                self.tab(name).bind("<<TabChanged>>", expose_bind_fns[i])
            except:
                pass


def run_app(**kwargs):
    app = GCG(**kwargs)
    app.mainloop()
    app.withdraw()
