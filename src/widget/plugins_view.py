#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Hou Shaohui
# 
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou Shaohui <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
import pango
import locale

from dtk.ui.new_treeview import TreeItem, TreeView
from dtk.ui.draw import draw_text, draw_pixbuf
from dtk.ui.utils import get_content_size
from dtk.ui.label import Label


from widget.ui_utils import (draw_single_mask, draw_alpha_mask,
                             set_widget_gravity)
from widget.skin import app_theme
from nls import _
import utils

class PluginItem(TreeItem):
    
    def __init__(self, plugin, pluginfo, enabled):
        TreeItem.__init__(self)
        self.column_index = 0
        self.side_padding = 5
        self.item_height = 25
        self.pluginfo = pluginfo
        self.version_width = 60
        self.enable_width = 60
        self.name_width = -1
        self.block_width = 10
        
        self.draw_padding_x = 5
        self.enabled = enabled
        self.plugin = plugin
        self.enabled_normal_dpixbuf = app_theme.get_pixbuf("webcast/collect_normal.png")
        self.enabled_press_dpixbuf = app_theme.get_pixbuf("webcast/collect_press.png")
        
        
    def get_height(self):    
        return self.item_height
    
    def get_column_widths(self):
        return [ self.name_width, self.version_width, self.enable_width, self.block_width]
    
    def get_column_renders(self):
        return (self.render_name, self.render_version, self.render_enabled, self.render_block)
    
    def unselect(self):
        self.is_select = False
        self.emit_redraw_request()
        
    def emit_redraw_request(self):    
        if self.redraw_request_callback:
            self.redraw_request_callback(self)
            
    def select(self):        
        self.is_select = True
        self.emit_redraw_request()
        
    def render_name(self, cr, rect):        
        # Draw select background.
        if self.is_select:    
            draw_single_mask(cr, rect.x, rect.y, rect.width, rect.height, "globalItemSelect")
        elif self.is_hover:
            draw_single_mask(cr, rect.x, rect.y, rect.width, rect.height, "globalItemHover")
        
        if self.is_select:
            text_color = "#FFFFFF"
        else:    
            text_color = app_theme.get_color("labelText").get_color()
            
        draw_text(cr, self.pluginfo["Name"], rect.x + self.draw_padding_x,
                  rect.y, rect.width - self.draw_padding_x * 2, 
                  rect.height, text_size=10, 
                  text_color = text_color,
                  alignment=pango.ALIGN_LEFT)    
        
    def render_version(self, cr, rect):    
        if self.is_select:    
            draw_single_mask(cr, rect.x, rect.y, rect.width, rect.height, "globalItemSelect")
        elif self.is_hover:
            draw_single_mask(cr, rect.x, rect.y, rect.width, rect.height, "globalItemHover")
        
        if self.is_select:
            text_color = "#FFFFFF"
        else:    
            text_color = app_theme.get_color("labelText").get_color()
            
        draw_text(cr, self.pluginfo["Version"], rect.x + self.draw_padding_x, 
                  rect.y, rect.width - self.draw_padding_x * 2,
                  rect.height, text_size=10, 
                  text_color = text_color,
                  alignment=pango.ALIGN_LEFT)    
    
    def render_enabled(self, cr, rect):
        if self.is_select:    
            draw_single_mask(cr, rect.x, rect.y, rect.width, rect.height, "globalItemSelect")
        elif self.is_hover:
            draw_single_mask(cr, rect.x, rect.y, rect.width, rect.height, "globalItemHover")
            
        if self.enabled:    
            pixbuf = self.enabled_press_dpixbuf.get_pixbuf()
        else:    
            pixbuf = self.enabled_normal_dpixbuf.get_pixbuf()
            
        icon_x = rect.x + (rect.width - pixbuf.get_width()) / 2
        icon_y = rect.y + (rect.height - pixbuf.get_height()) / 2
        draw_pixbuf(cr, pixbuf, icon_x, icon_y)
    
    def render_block(self, cr, rect):
        if self.is_select:    
            draw_single_mask(cr, rect.x, rect.y, rect.width, rect.height, "globalItemSelect")
        elif self.is_hover:
            draw_single_mask(cr, rect.x, rect.y, rect.width, rect.height, "globalItemHover")
            
    def toggle_enabled(self):        
        if self.enabled:
            self.enabled = False
        else:    
            self.enabled = True
        self.emit_redraw_request()    
    
    def unhover(self, column, offset_x, offset_y):
        self.is_hover = False
        self.emit_redraw_request()
    
    def hover(self, column, offset_x, offset_y):
        self.is_hover = True
        self.emit_redraw_request()
        
class PluginsManager(gtk.VBox):
    
    def __init__(self):
        gtk.VBox.__init__(self)
        
        self.set_spacing(5)
        self.plugins = utils.get_main_window().plugins
        self.plugins_view = TreeView()
        self.plugins_view.draw_mask = self.plugins_view_draw_mask
        self.plugins_view.set_size_request(420, 300)        
        self.plugins_view.connect("single-click-item", self.on_plugins_view_single_click)
                
        self.plugins_view.set_column_titles([_("插件"), _("版本"), _("启用"), ""],
                                            (self.sort_by_title, self.sort_by_title,
                                             self.sort_by_title, self.sort_by_title))
        plugins_view_align = set_widget_gravity(self.plugins_view, gravity=(1, 1, 1, 1),
                                                paddings=(10, 0, 0, 0))

        self.__load_plugin_list()
        
        
        # plugin info
        self.plugin_name = Label("")
        self.plugin_name.set_size_request(410, 25)
        self.plugin_authors = Label("")
        self.plugin_authors.set_size_request(410, 25)
        self.plugin_description = Label("")
        self.plugin_description.set_size_request(410, 60)
        
        self.pack_start(plugins_view_align, False, True)
        
        self.pack_start(self.plugin_name, False, True)
        self.pack_start(self.plugin_authors, False, True)
        self.pack_start(self.plugin_description, False, True)
        
        
    def sort_by_title(self, items, reverse):    
        return sorted(items, key=lambda item: item.plugin, reverse=reverse)
    
    def plugins_view_draw_mask(self, cr, x, y, width, height):
        draw_alpha_mask(cr, x, y, width, height, "layoutLeft")
        
    def __load_plugin_list(self):    
        
        # clear plugins_view items.
        # self.plugins_view.clear()
        
        plugins = self.plugins.list_installed_plugins()
        plugins_list = []
        failed_list = []
        
        for plugin in plugins:
            try:
                info = self.plugins.get_plugin_info(plugin)
            except Exception:    
                failed_list.append(plugin)
                continue
            
            enabled  = plugin in self.plugins.enabled_plugins
            plugins_list.append((plugin, info, enabled))
            
        plugins_list.sort(key=lambda x: locale.strxfrm(x[1]["Name"]))
        plugins_items = [PluginItem(*args) for args in plugins_list]
        self.plugins_view.add_items(plugins_items)
        
    def on_plugins_view_single_click(self, widget, item, column, x, y):
        if column == 2:
            plugin = item.plugin
            will_enable = not item.enabled
            if will_enable:
                try:
                    self.plugins.enable_plugin(plugin)
                except Exception, e:    
                    print e
                    return
            else:    
                try:
                    self.plugins.disable_plugin(plugin)
                except Exception, e:    
                    print e
                    return
            item.toggle_enabled()    
            
        plugin_name = "<b>%s: </b>%s" % (_("插件"), item.pluginfo["Name"])    
        plugin_authors = "<b>%s: </b>%s" % (_("插件作者"), 
                                                         " ".join(item.pluginfo["Authors"]))
        plugin_des = item.pluginfo["Description"]        
        self.plugin_name.set_text(plugin_name)
        self.plugin_authors.set_text(plugin_authors)
        self.plugin_description.set_text(plugin_des)

