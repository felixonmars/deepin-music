/*
 * Copyright (C) 2016 ~ 2018 Wuhan Deepin Technology Co., Ltd.
 *
 * Author:     Iceyer <me@iceyer.net>
 *
 * Maintainer: Iceyer <me@iceyer.net>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

#include <QScopedPointer>
#include <DTitlebar>
#include <DWidget>
#include <QStackedLayout>
#include <QVBoxLayout>
#include <DGuiApplicationHelper>
#include <DMainWindow>

DWIDGET_USE_NAMESPACE

class TitlebarWidget;
class FooterWidget;
class MusicContentWidget;
class SearchResult;
class MusicLyricWidget;
class ImportWidget;
class QShortcut;
class DequalizerDialog;
class MainFrame : public DMainWindow
{
    Q_OBJECT
public:
    explicit MainFrame();
    ~MainFrame() Q_DECL_OVERRIDE;

    void initUI(bool showLoading);
    MusicContentWidget *getMusicContentWidget();
    // 启动自动播放和进度条设置
    void autoStartToPlay();
public slots:
    // 显示弹窗消息
    void showPopupMessage(const QString &songListName, int selectCount, int insertCount);
private:
    /**
     * @brief initMenuAndShortCut
     */
    void initMenuAndShortcut();

private slots:
    void slotTheme(DGuiApplicationHelper::ColorType themeType);
    void slotSearchEditFoucusIn();
    void slotLyricClicked();
    void slotImportFinished();
    void slotShortCutTriggered();
    void slotMenuTriggered(QAction *action);
    void slotSwitchTheme();
    // 所有歌曲被删除
    void slotAllMusicCleared();
    // 延迟自动播放
    void slotAutoPlay(bool bremb);
    // 文管打开文件
    void slotPlayFromFileMaganager();
protected:
    virtual void showEvent(QShowEvent *event) Q_DECL_OVERRIDE;
    virtual void enterEvent(QEvent *event) Q_DECL_OVERRIDE;
    virtual void resizeEvent(QResizeEvent *e) Q_DECL_OVERRIDE;
    virtual void closeEvent(QCloseEvent *event) Q_DECL_OVERRIDE;
//    virtual void paintEvent(QPaintEvent *e) Q_DECL_OVERRIDE;
private:
    DTitlebar           *m_titlebar = nullptr;
    TitlebarWidget      *m_titlebarwidget = nullptr;
    FooterWidget        *m_footer = nullptr;
    MusicContentWidget  *m_musicContentWidget = nullptr;
    SearchResult        *m_searchResult = nullptr;
    MusicLyricWidget    *m_musicLyricWidget = nullptr;
    ImportWidget        *m_importWidget = nullptr;
    DequalizerDialog    *m_dequalizerDialog = nullptr;
    //mainframe action
    QAction             *m_newSonglistAction    = nullptr;
    QAction             *m_addMusicFiles        = nullptr;
    QAction             *m_equalizer            = nullptr;
    //QAction             *m_colorModeAction      = nullptr;
    //QAction             *m_exit                 = nullptr;
    QAction             *m_settings             = nullptr;
    QString             m_firstPlaySong = "";
    //short cut
    QShortcut           *addmusicfilesShortcut = nullptr;
    QShortcut           *viewshortcut = nullptr;
    QShortcut           *searchShortcut = nullptr;
    QShortcut           *windowShortcut = nullptr;
};

//extern const QString s_PropertyViewname;
//extern const QString s_PropertyViewnameLyric;

