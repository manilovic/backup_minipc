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
#include "qtapp.h"

#if defined(_linux_)
#include <sys/vfs.h>
#elif defined(_darwin_)
#include <sys/param.h>
#include <sys/mount.h>
#endif

uint64_t get_free_space(const utf8_t* Folder)
{
    uint64_t fspace;
    struct statfs st;

    fspace=0;
    fspace--;

    if (statfs(Folder,&st))
    {
        return 0;
    }

    fspace = st.f_bavail;
    fspace *= st.f_bsize;

    return fspace;
}

