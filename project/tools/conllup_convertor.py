def convert_conllup(conllup_path: str, final_path: str) -> None:
    """
    create new conllu file from conllup file.
    Basically keeps first 10 columns
    """

    with open(conllup_path, 'rb') as conllup,\
         open(final_path, 'ab') as conllu:

        conllup_mv = memoryview(conllup.read())

        pnt = 0
        while pnt < len(conllup_mv):
            lst_pnt = pnt
            if conllup_mv[pnt] == 35: # '#'
                while lst_pnt < len(conllup_mv) and\
                      conllup_mv[lst_pnt] != 10: # '\n'
                    lst_pnt += 1

                line = conllup_mv[pnt:lst_pnt]
                conllu.write(line)
                conllu.write(b'\n')

            elif conllup_mv[lst_pnt] == (10, 13): # '\n' '\r'
                continue

            else:
                v_tab_count = 0
                while v_tab_count < 9:
                    if conllup_mv[lst_pnt] in (10, 13): # '\n', '\r'
                        break
                    if conllup_mv[lst_pnt] == 9: # '\t'
                        v_tab_count += 1
                    lst_pnt += 1

                while conllup_mv[lst_pnt] not in (9, 10, 13): # '\t', '\n', '\r'
                    lst_pnt += 1

                line = conllup_mv[pnt:lst_pnt]
                conllu.write(line)
                conllu.write(b'\n')

                while lst_pnt < len(conllup_mv) and\
                      conllup_mv[lst_pnt] != 10: # '\n'
                    lst_pnt += 1

            pnt = lst_pnt + 1
        del conllup_mv
