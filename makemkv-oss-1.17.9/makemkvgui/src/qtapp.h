/*
    MakeMKV GUI - Graphics user interface application for MakeMKV

    Copyright (C) 2007-2025 GuinpinSoft inc <makemkvgui@makemkv.com>

    You may use this file in accordance with the end user license
    agreement provided with the Software. For licensing terms and
    conditions see License.txt

    This Software is distributed on an "AS IS" basis, WITHOUT WARRANTY
    OF ANY KIND, either express or implied. See the License.txt for
    the specific language governing rights and limitations.

*/
#ifndef APP_QTAPP_H
#define APP_QTAPP_H

#include "qtgui.h"
#include <lgpl/aproxy.h>

#define QT_C_ASSERT(e) typedef char __QT_C_ASSERT__[(e)?1:-1]
#define _qt_countof(a) (sizeof(a)/sizeof(*(a)))

#include "qtstr.h"

class QSimpleLabel : public QLabel
{
public:
    QSimpleLabel() : QLabel()
    {
        setTextFormat(Qt::PlainText);
        setWordWrap(false);
    }
};

class QGrayTextViewer : public QTextEdit
{
    QString cachedText;
public:
    QGrayTextViewer()
    {
        setReadOnly(true);
        setLineWrapMode(QTextEdit::NoWrap);
    }
    void setHtmlBody(const QString& str);
    void rebuildHtmlBody();
};

static inline QLabel* createLabel(const QString &txt)
{
    QLabel* t = new QSimpleLabel();
    t->setText(txt);
    return t;
}

static inline QFrame* createHLine()
{
    QFrame *hline = new QFrame();
    hline->setFrameStyle(QFrame::HLine | QFrame::Sunken);
    return hline;
}

void AppendGrayBodyTag(QString &str,const QWidget *widget);

QString FormatDiskFreeSpace(const utf8_t* FolderName);

QString GetInfo(AP_UiItem* item,AP_ItemAttributeId Id);
QString BuildItemInfo(AP_UiItem *Item,bool expertMode);

QImage* getBuiltinImage(unsigned int id);
QIcon* createIconPixmaps(unsigned int firstId,unsigned int count);
void createAnimIcons();
const QIcon* getAnimIcon(unsigned int id,unsigned int id2);
QSize getImageGoodSize(int height, bool biggerOk);
QSize getIconSize(unsigned int den);


void check(const QMetaObject::Connection& connection);


#endif // APP_QTAPP_H
