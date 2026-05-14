import struct

def unescape(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            c = s[i+1]
            if c == 'n':
                result.append('\n')
            elif c == 't':
                result.append('\t')
            elif c == '"':
                result.append('"')
            elif c == '\\':
                result.append('\\')
            else:
                result.append('\\')
                result.append(c)
            i += 2
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)


def compile_po(po_path, mo_path):
    entries = {}
    current_id = None
    current_str = None
    in_msgid = False
    in_msgstr = False

    with open(po_path, encoding='utf-8') as f:
        lines = f.readlines()

    def flush():
        nonlocal current_id, current_str
        if current_id is not None and current_str is not None:
            entries[unescape(current_id)] = unescape(current_str)
        current_id = None
        current_str = None

    for line in lines:
        line = line.rstrip('\n')
        if line.startswith('msgid '):
            flush()
            in_msgid = True
            in_msgstr = False
            current_id = line[7:-1]
        elif line.startswith('msgstr '):
            in_msgid = False
            in_msgstr = True
            current_str = line[8:-1]
        elif line.startswith('"') and in_msgid:
            current_id += line[1:-1]
        elif line.startswith('"') and in_msgstr:
            current_str += line[1:-1]
    flush()

    entries = {k: v for k, v in entries.items() if v or k == ''}

    keys = sorted(entries.keys())
    values = [entries[k] for k in keys]

    koffsets = []
    voffsets = []
    kdata = b''
    vdata = b''
    for k, v in zip(keys, values):
        kb = k.encode('utf-8')
        vb = v.encode('utf-8')
        koffsets.append((len(kb), len(kdata)))
        voffsets.append((len(vb), len(vdata)))
        kdata += kb + b'\x00'
        vdata += vb + b'\x00'

    n = len(keys)
    header_size = 28
    key_table_offset = header_size
    val_table_offset = key_table_offset + n * 8
    key_data_offset = val_table_offset + n * 8
    val_data_offset = key_data_offset + len(kdata)

    output = struct.pack('<IIIIIII',
        0x950412de, 0, n,
        key_table_offset, val_table_offset,
        0, val_data_offset + len(vdata))
    for length, offset in koffsets:
        output += struct.pack('<II', length, key_data_offset + offset)
    for length, offset in voffsets:
        output += struct.pack('<II', length, val_data_offset + offset)
    output += kdata
    output += vdata

    with open(mo_path, 'wb') as f:
        f.write(output)
    print(f'Compiled {po_path} ({n} entries)')


base = 'C:/Users/C#/Workspace 911/StuLance/locale'
for lang in ['fr', 'ar']:
    compile_po(f'{base}/{lang}/LC_MESSAGES/django.po', f'{base}/{lang}/LC_MESSAGES/django.mo')
