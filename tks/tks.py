import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk

# Global variables
g_DEBUG = 0

FRAME_PAD_X=1
FRAME_PAD_Y=1

WIDGET_PAD_X=1
WIDGET_PAD_Y=1

LABEL_WIDTH=10
ENTRY_WIDTH=40

TEXT_WIDTH=40
TEXT_HEIGHT=10

# ToDo
# 1. Add set function for default vales - and parameterize width, height
# 2. Better way to list default values - may be enum
# 3. Add image widget
# 4. Add drop down list
# 5. Add drop down list widget with values get added as entered by user
# 6. Add List item seletion widgte width scorll bars
# 7. * Fix imagepack function to remove self varibales (should not be based on index for sure)

# Utlity for creating TkInter GUI Applications
class Tks():
    def __init__(self, title = "", width=600, height=400):
        # Create root frame
        self.frame_root = tk.Tk()
        self.frame_root.title(title)
        self.frame_root.geometry(f"{width}x{height}")
        self.frame_root.minsize(width, height)

        # Create top frame
        self.frame_top = self.CreateFrame(self.frame_root)['frame']
        self.check_button_var_dict = {}
        self.check_combobox_var_dict = {}
        self.check_combobox_values_dict = {}
        self.check_dateentry_values_dict = {}
        self.store_treeview_items_dict = {}
        self.store_treeview_sorted_column = {}
        self.store_imagepack_label_list = []
        return 

    # -------------------------------------------------------------------------
    # Get Default values
    def GetDeafultFramePadX(self):
        return(FRAME_PAD_X)
    def GetDeafultFramePadY(self):
        return(FRAME_PAD_Y)
    def GetDeafultWidgetPadY(self):
        return(WIDGET_PAD_X)
    def GetDeafultWidgetPadY(self):
        return(WIDGET_PAD_Y)
    def GetDeafultLabelWidth(self):
        return(LABEL_WIDTH)
    def GetDeafultEntryWidth(self):
        return(ENTRY_WIDTH)
    def GetDeafultTextWidth(self):
        return(TEXT_WIDTH)
    def GetDeafultTextHeight(self):
        return(TEXT_HEIGHT)

    # -------------------------------------------------------------------------
    def GetFrameRoot(self):
        return self.frame_root
    
    def GetFrameTop(self):
        return self.frame_top

    # -------------------------------------------------------------------------
    def PackFrame(self, frame, padx=FRAME_PAD_X, pady=FRAME_PAD_Y, side="", fill=tk.X, expand="", debug=0):
        frame.pack(padx=padx, pady=pady)
        if (side != ""): frame.pack(side=side)
        if (fill != ""): frame.pack(fill=fill)
        if (expand != ""): frame.pack(expand=expand)
        if (g_DEBUG or debug):
            print(f"Frame side:'{side}' fill:'{fill}' expand:'{expand}'")
        return

    def CreateFrame(self, root, side=tk.LEFT, fill="", expand =""):
        frame = tk.Frame(root)
        frame.pack(padx=FRAME_PAD_X, pady=FRAME_PAD_Y, fill=tk.X)
        return {'frame':frame}

    def PackWidget(self, wgt, padx=FRAME_PAD_X, pady=FRAME_PAD_Y, side=tk.LEFT, fill="", expand ="", debug=0):
        wgt.pack(padx=WIDGET_PAD_X, pady=WIDGET_PAD_Y)
        if (side != ""): wgt.pack(side=side)
        if (fill != ""): wgt.pack(fill=fill)
        if (expand != ""): wgt.pack(expand=expand)
        if (g_DEBUG or debug):
            print(f"Widget side:'{side}' fill:'{fill}' expand:'{expand}'")
        return

    # -------------------------------------------------------------------------
    def CreateFrameGrid(self, root, frame_grid_info, debug=0):
        num_rows=frame_grid_info['rows']
        num_cols=frame_grid_info['cols']
        frame_list = []
        for r in range(num_rows):
            for c in range(num_cols):
                frame = tk.Frame(root, borderwidth=2, relief="ridge", padx=10, pady=10)
                frame.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

                # Optional: Fill each frame with a label or widgets
                if (g_DEBUG or debug):
                    label = tk.Label(frame, text=f"Frame {r},{c}", font=("Arial", 12))
                    label.pack()

                # Save frame if needed later
                frame_list.append(frame)

        # Make the grid expand with window resize
        for r in range(self.rows):
            root.grid_rowconfigure(r, weight=1)
        for c in range(self.cols):
            root.grid_columnconfigure(c, weight=1)
        return {'frame_list':frame_list}

    def CreateFramePack(self, root, frame_grid_info, debug=0):
        num_rows=frame_grid_info['rows']
        num_cols=frame_grid_info['cols']
        frame_list = []
        for r in range(num_rows):
            row_frame = tk.Frame(root)
            row_frame.pack(side="top", fill="both", expand=True)

            for c in range(num_cols):
                cell_frame = tk.Frame(
                    row_frame, borderwidth=2, relief="ridge", padx=10, pady=10
                )
                cell_frame.pack(side="left", fill="both", expand=True)

                if (g_DEBUG or debug):
                    # Optional: add content to each cell
                    label = tk.Label(cell_frame, text=f"Frame {r},{c}")
                    label.pack()

                # Save frame if needed later
                frame_list.append(cell_frame)
        return {'frame_list':frame_list}

    # -------------------------------------------------------------------------
    def CreateFramedEntry(self, root, label_str, entry_width=''):
        frame = tk.Frame(root)
        self.PackFrame(frame)
        label = tk.Label(frame, text=label_str, width=LABEL_WIDTH+15)
        self.PackWidget(label)
        if (entry_width == ''): entry_width = ENTRY_WIDTH-10
        entry = tk.Entry(frame, width=entry_width)
        self.PackWidget(entry)
        return {'frame':frame, 'label':label, 'entry':entry}

    # -------------------------------------------------------------------------
    def CreateFramedFileSelect(self, root, label_str, button_str, cmd):
        frame = tk.Frame(root)
        self.PackFrame(frame)
        label = tk.Label(frame, text=label_str, width=LABEL_WIDTH)
        self.PackWidget(label)
        entry = tk.Entry(frame, width=40)
        self.PackWidget(entry)
        button = tk.Button(frame, text=button_str, command=cmd)
        self.PackWidget(button)
        return {'frame':frame, 'label':label, 'entry':entry, 'button':button}

    # -------------------------------------------------------------------------
    def CreateFramedButtons(self, root, label_str, button_list,
                            side=tk.LEFT, fill="", expand =""):
        frame = tk.Frame(root)
        self.PackFrame(frame)
        label = ''
        if (label_str != ""):
            label = tk.Label(frame, text=label_str, width=LABEL_WIDTH)
            self.PackWidget(label)
        for button in button_list:
            button = tk.Button(frame, command=button['command'], text=button['text'])
            self.PackWidget(button, side=side, fill=fill, expand=expand)
        return {'frame':frame, 'label':label, 'button':button}

    # -------------------------------------------------------------------------
    def CreateFramedCheckButtons(self, root, label_str, chk_button_param_list,
                                 side=tk.LEFT, fill="", expand =""):
        frame = tk.Frame(root)
        self.PackFrame(frame)
        label = ''
        if (label_str != ""):
            label = tk.Label(frame, text=label_str, width=LABEL_WIDTH)
            self.PackWidget(label)
        chk_button_wgt_list = []
        for chk_button in chk_button_param_list:
            text=chk_button['text']
            var_name=chk_button['var']
            var = tk.BooleanVar()
            chk_button_wgt = tk.Checkbutton(frame, text=text, variable=var)
            self.check_button_var_dict.update({var_name:var})
            chk_button_wgt_list.append(chk_button_wgt)
            self.PackWidget(chk_button_wgt, side=side, fill=fill, expand=expand)
        return {'frame':frame, 'label':label, 'check_button':chk_button_wgt_list}
        
    # -------------------------------------------------------------------------
    def CreateFramedTextWithScrollBar(self, root):
        frame = tk.Frame(root)
        self.PackFrame(frame, fill=tk.BOTH, expand=1)
        text = tk.Text(frame, height=TEXT_HEIGHT, width=TEXT_WIDTH, wrap=tk.WORD, state=tk.DISABLED)
        self.PackWidget(text, fill=tk.BOTH, expand=1)
        scrollbar = tk.Scrollbar(frame, command=text.yview)
        self.PackWidget(scrollbar, side=tk.RIGHT, fill=tk.Y)
        text.config(yscrollcommand=scrollbar.set)
        return {'frame':frame, 'text':text, 'scrollbar':scrollbar}

    # -------------------------------------------------------------------------
    def AddDropdownItem(self, event, wgt, var_name):
        var = self.check_combobox_var_dict[var_name]
        options = self.check_combobox_values_dict[var_name]
        opt = var.get().strip()
        if opt and opt not in options:
            self.check_combobox_values_dict[var_name].append(opt)
            wgt["values"] = self.check_combobox_values_dict[var_name]

    # -------------------------------------------------------------------------
    def CreateDropdownList(self, root, label_str, dropdown_info, auto_add=False):
        frame = tk.Frame(root)
        self.PackFrame(frame, fill=tk.BOTH, expand=1)
        label = tk.Label(frame, text=label_str, width=LABEL_WIDTH)
        self.PackWidget(label)
        var_name = dropdown_info['var']
        var = tk.StringVar()
        options = dropdown_info['values']
        dropdown = ttk.Combobox(frame, textvariable=var, values=options, state='readonly')
        if auto_add == False:
            dropdown = ttk.Combobox(frame, textvariable=var, values=options, state='readonly')
        else:
            dropdown = ttk.Combobox(frame, textvariable=var)
            dropdown.bind("<Return>", lambda event: self.AddDropdownItem(event, dropdown, var_name))
        self.check_combobox_var_dict.update({var_name:var})
        self.check_combobox_values_dict.update({var_name:options})
        self.PackWidget(dropdown, fill=tk.X, expand=1)
        return {'frame':frame, 'label':label, 'combobox':dropdown}

    # -------------------------------------------------------------------------
    def CreateDateEntry(self, root, label_str, date_entry_info):
        frame = tk.Frame(root)
        self.PackFrame(frame)
        label = tk.Label(frame, text=label_str, width=LABEL_WIDTH)
        self.PackWidget(label)
        date_wgt = DateEntry(frame)
        self.PackWidget(date_wgt)
        var_name = date_entry_info['var']
        self.check_dateentry_values_dict.update({var_name:date_wgt})
        return {'frame':frame, 'label':label, 'dateentry':date_wgt}

    # -------------------------------------------------------------------------
    def CreateImagePack(self, root, image_grid_info):
        rows=image_grid_info['rows']
        cols=image_grid_info['cols']
        image_paths=image_grid_info['image_paths']
        return_widgets = self.build_image_pack(root, rows, cols, image_paths)
        root.bind("<Configure>", lambda event: self.on_resize_image_pack(event, root, rows, cols, image_paths))
        return(return_widgets)

    def build_image_pack(self, root, rows, cols, image_paths):
        self.store_imagepack_label_list = []
        label_list = []
        frame_list = []
        idx = 0
        for r in range(rows):
            row_frame = tk.Frame(root)
            row_frame.pack(side="top", fill="both", expand=True)

            for c in range(cols):
                if idx < len(image_paths):
                    img = Image.open(image_paths[idx])
                    # self.original_images.append(img)

                    img_frame = tk.Frame(row_frame, borderwidth=0, relief="solid")
                    img_frame.pack(side="left", fill="both", expand=True)

                    label = tk.Label(img_frame)
                    label.pack(fill="both", expand=True)
                    self.store_imagepack_label_list.append((label, img))
                    label_list.append((label, img))
                    frame_list.append(img_frame)
                    idx += 1
        return {'frame_list':frame_list, 'label_list':label_list}

    def on_resize_image_pack(self, event, root, rows, cols, image_paths):
        if event.widget == root:
            # Get the current window size
            window_width = event.width
            window_height = event.height
            # print(f"Window: width:{window_width} height:{window_height}")

            # Calculate the new image size based on window size
            new_width = int(window_width / cols)
            new_height = int(window_height / rows)
            # print(f"Image: width:{new_width} height:{new_height}")

            # Resize each image to fit the new size
            for idx, (label, original) in enumerate(self.store_imagepack_label_list):
                resized_img = original.resize((new_width, new_height))
                photo = ImageTk.PhotoImage(resized_img)
                label.configure(image=photo)
                label.image = photo  # Prevent garbage collection
        return

    # -------------------------------------------------------------------------
    def CreateScolledItemList(self, root, scrolled_item_info):
        # Frame for the treeview and scrollbar
        title = scrolled_item_info['title']
        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Scrollbar for the Treeview
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        # Treeview to display the list (with multiple columns)
        headings = scrolled_item_info['headings']
        column_headings=[hinfo[0] for hinfo in headings]
        # print(f"ColumnHeadings: {column_headings}")
        treeview = ttk.Treeview(frame, columns=column_headings, show="headings", selectmode="extended")
        treeview.pack(fill="both", expand=True)

        # Configure columns and headings
        idx = 0
        for hinfo in headings:
            name = hinfo[0]
            width = hinfo[1]
            anchor = hinfo[2]
            # print(f"hinfo:{hinfo} name:{name} width:{width} anchor:{anchor}" )
            treeview.heading(name, text=name, command=lambda: self.sort_column_scrolled_itemlist(title, column_headings, treeview, name, idx))
            treeview.column(name, width=width)
            if anchor != '':
                treeview.column(name, anchor=anchor)
            idx+=1

        # Attach scrollbar to treeview
        scrollbar.config(command=treeview.yview)
        treeview.config(yscrollcommand=scrollbar.set)

        # Populate the Treeview with initial items
        items = scrolled_item_info['items']
        for item in items:
            treeview.insert("", "end", values=item)

        self.store_treeview_items_dict.update({title:items})
        self.store_treeview_sorted_column.update({title:''})

        return {'frame':frame, 'treeview':treeview, 'scrollbar':scrollbar}

    def sort_column_scrolled_itemlist(self, title, column_headings, treeview, column, idx):
        # Sort the items by the selected column
        # print(f"Pre: {self.store_treeview_items_dict}")
        index = column_headings.index(column)
        # print(f"column_headings:{column_headings}, column:{column} Index:{index} Idx:{idx}")
        items = self.store_treeview_items_dict[title]
        sorted_column = self.store_treeview_sorted_column[title]
        items.sort(key=lambda x: x[index].lower(), reverse=sorted_column == column)

        # Update the sorted column
        self.store_treeview_sorted_column=({title:column})

        # Clear the existing list and re-insert the sorted items
        for row in treeview.get_children():
            treeview.delete(row)

        for item in items:
            treeview.insert("", "end", values=item)

        self.store_treeview_items_dict.update({title:items})
        # print(f"Post: {self.store_treeview_items_dict}")
        return

    # -------------------------------------------------------------------------