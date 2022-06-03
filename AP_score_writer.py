import argparse as ap
import datetime as dt
import pathlib

NUMBER_OF_AP_EXAMS = 30
exam_sets = range(1,NUMBER_OF_AP_EXAMS+1)

def ap_file_def() -> list:
    """
    returns a list the column names and column specs for the AP Scores fixed width data file
    """
    ap_def = [
        ["AP_ID",                        1,   8,  8],
        ["last_name",                    9,  23, 15],
        ["first_name",                  24,  35, 12],
        ["middle_initial",              36,  36,  1],
        ["street_address_1",            37,  66, 30],
        ["street_address_2",            67,  96, 30],
        ["street_address_3",            97, 126, 30],
        ["state",                      127, 128,  2],
        ["zip_code",                   129, 137,  9],
        ["country_code",               138, 140,  3],
        ["gender",                     141, 141,  1],
        ["birth_date",                 142, 147,  6],
        ["filler_1",                   148, 156,  9],
        ["education_level",            157, 157,  1],
        ["expected_college_entrance",  158, 160,  3],
        ["filler_2",                   161, 161,  1],
        ["student_search",             162, 162,  1],
        ["best_language",              163, 163,  1],
        ["apply_soph_standing",        164, 164,  1],
        ["filler_3",                   165, 172,  8],
        ["previous_ai_year_1",         173, 174,  2],
        ["previous_ai_code_1",         175, 180,  6],
        ["previous_ai_year_2",         181, 182,  2],
        ["previous_ai_code_2",         183, 188,  6],
        ["award_type_1",               189, 190,  2],
        ["award_year_1",               191, 192,  2],
        ["award_type_2",               193, 194,  2],
        ["award_year_2",               195, 196,  2],
        ["award_type_3",               197, 198,  2],
        ["award_year_3",               199, 200,  2],
        ["award_type_4",               201, 202,  2],
        ["award_year_4",               203, 204,  2],
        ["award_type_5",               205, 206,  2],
        ["award_year_5",               207, 208,  2],
        ["award_type_6",               209, 210,  2],
        ["award_year_6",               211, 212,  2],
        ["hs_school_code",             213, 218,  6],
        ["hs_contact_name",            219, 248, 30],
        ["hs_institution_name",        249, 278, 30],
        ["hs_street_address_1",        279, 308, 30],
        ["hs_street_address_2",        309, 338, 30],
        ["hs_street_address_3",        339, 368, 30],
        ["hs_state",                   369, 370,  2],
        ["hs_zip_code",                371, 375,  5],
        ["col_school_code",            376, 381,  6],
        ["col_contact_name",           382, 411, 30],
        ["col_institution_name",       412, 441, 30],
        ["col_street_address_1",       442, 471, 30],
        ["col_street_address_2",       472, 501, 30],
        ["col_street_address_3",       502, 531, 30],
        ["col_state",                  532, 533,  2],
        ["col_zip_code",               534, 538,  5],
    ]

    # Exam Sets
    col_begin = 539
    exam_cols = [
        ["_admin_year",              2],
        ["_exam_code",               2],
        ["_exam_score",              1],
        ["_irr_code_1",              2],
        ["_irr_code_2",              2],
        ["_exam_suppression_flag",   1],
        ["_class_section_code",      1],
    ]
    for s in exam_sets:
        ss = f"{s:02d}"
        # print(f"{s,ss}")
        for c in exam_cols:
            col_name = f"ex{ss}{c[0]}"
            col_width = c[1]
            start_col = col_begin
            end_col = col_begin + (col_width - 1)
            # print(f"[{col_name}, {start_col}, {end_col}, {col_width}]")
            ap_def.append([col_name, start_col, end_col, col_width])
            col_begin = end_col + 1

    ap_cols2 = [
        ["scores_released_date",        869, 874,  6],
        ["student_update_date",         875, 880,  6],
        ["report_date",                 881, 886,  6],
        ["service_type",                887, 888,  2],
        ["service_code",                889, 892,  4],
        ["ordering_institution_key",    893, 900,  8],
        ["race-ethnicity_student_resp", 901, 911, 11],
        ["filler_4",                    912, 933, 22],
        ["race-ethnicity_derived",      934, 935,  2],
        ["filler_5",                    936, 950, 15],
    ]
    ap_def.extend(ap_cols2)

    # check column consistency
    prev_pos = 0
    for f in ap_def:
        if (prev_pos + 1) != f[1]:
            raise ValueError(f"ap_file_def(): incorrect start position: {f[0]}, start: {f[1]}, previous: {prev_pos}")
        if (f[2]-f[1]+1) != f[3]:
            raise ValueError(f"ap_file_def(): incorrect width: {f[0]}, start: {f[1]}, end: {f[2]}, width: {f[3]}")
        prev_pos = f[2]    

    return ap_def


def ap_exam_names() -> tuple[dict, int]:
    """ 
    returns a dict of AP exam names and an int with the maximum exam name string length
    """
    exam_name = {
        '07': 'UNITED STATES HISTORY',
        '13': 'ART HISTORY',
        '14': 'DRAWING',
        '15': '2D ART AND DESIGN',
        '16': '3D ART AND DESIGN',
        '20': 'BIOLOGY',
        '22': 'SEMINAR',
        '23': 'RESEARCH',
        '25': 'CHEMISTRY',
        '28': 'CHINESE LANGUAGE AND CULTURE',
        '31': 'COMPUTER SCIENCE A',
        '32': 'COMPUTER SCIENCE PRINCIPLES',
        '34': 'ECONOMICS: MICROECONOMICS',
        '35': 'ECONOMICS: MACROECONOMICS',
        '36': 'ENGLISH LANGUAGE AND COMPOSITION',
        '37': 'ENGLISH LITERATURE AND COMPOSITION',
        '40': 'ENVIRONMENTAL SCIENCE',
        '43': 'EUROPEAN HISTORY',
        '48': 'FRENCH LANGUAGE AND CULTURE',
        '53': 'HUMAN GEOGRAPHY',
        '55': 'GERMAN LANGUAGE AND CULTURE',
        '57': 'GOVERNMENT AND POLITICS: UNITED STATES',
        '58': 'GOVERNMENT AND POLITICS: COMPARATIVE',
        '60': 'LATIN',
        '62': 'ITALIAN LANGUAGE AND CULTURE',
        '64': 'JAPANESE LANGUAGE AND CULTURE',
        '66': 'CALCULUS AB',
        '68': 'CALCULUS BC',
        '69': '-CALCULUS AB SUBSCORE',
        '75': 'MUSIC THEORY',
        '76': '-AURAL SUBSCORE',
        '77': '-NONAURAL SUBSCORE',
        '78': 'PHYSICS B',
        '80': 'PHYSICS C: MECHANICS',
        '82': 'PHYSICS C: ELECTRICITY AND MAGNETISM',
        '83': 'PHYSICS 1',
        '84': 'PHYSICS 2',
        '85': 'PSYCHOLOGY',
        '87': 'SPANISH LANGUAGE AND CULTURE',
        '89': 'SPANISH LITERATURE AND CULTURE',
        '90': 'STATISTICS',
        '93': 'WORLD HISTORY: MODERN',
        
    }
    
    exam_name_width_max = 0
    for en in exam_name.values():
        if len(en) > exam_name_width_max:
            exam_name_width_max = len(en)
    
    return exam_name, exam_name_width_max


def row_dict(r: str, colspecs: dict) -> dict:
    """
    returns a dict of the values in one row defined by colspecs
    """
    # print(r)
    rd = {}
    for f in colspecs:
        # print(f, ap_colspecs[f], ap_colspecs[f][0], ap_colspecs[f][1])
        rd[f] = r[colspecs[f][0]:colspecs[f][1]]
    return rd


def write_ap_scores(ap_scores_file: pathlib.Path, output_file: pathlib.Path) -> None:
    """
    writes AP test scores from decrypted ap_scores_file to output_file and to stdout
    """
    ap_def = ap_file_def()

    ap_field_names = []
    ap_colspecs = {}
    ap_widths = {}
    for f in ap_def:
        ap_field_names.append(f[0])
        ap_colspecs[f[0]] = (f[1]-1, f[2])  # Column numbering is zero-based. Interval closed on left, open on right.
        ap_widths[f[0]] = f[3]

    exam_name, exam_name_width_max = ap_exam_names()

    student_count = 0

    with output_file.open('w') as f_out:
        print(f"AP Test Scores - {dt.datetime.now()}\n")
        f_out.write(f"AP Test Scores - {dt.datetime.now()}\n\n")

        with ap_scores_file.open('r') as f:
            lines = f.readlines()

            for l in lines:
    #             print(l)
                d = row_dict(l, colspecs=ap_colspecs)
    #             print(d)
    #             print()
                print(f"{d['last_name']:<{ap_widths['last_name']}} {d['first_name']:<{ap_widths['first_name']}} DOB:{d['birth_date'][:2]}/{d['birth_date'][2:4]}/{d['birth_date'][4:]}")
                f_out.write(f"{d['last_name']:<{ap_widths['last_name']}} {d['first_name']:<{ap_widths['first_name']}} DOB:{d['birth_date'][:2]}/{d['birth_date'][2:4]}/{d['birth_date'][4:]}\n")
                for s in exam_sets:
                    exam_code = f"ex{s:02d}_exam_code"
                    if d[exam_code]!='  ':
                        print(f"exam: {d[exam_code]} {exam_name[d[exam_code]]:<{exam_name_width_max}}year: {d[f'ex{s:02d}_admin_year']} score: {d[f'ex{s:02d}_exam_score']} ")
                        f_out.write(f"exam: {d[exam_code]} {exam_name[d[exam_code]]:<{exam_name_width_max}}year: {d[f'ex{s:02d}_admin_year']} score: {d[f'ex{s:02d}_exam_score']} \n")

                student_count += 1 
                print(" -" * 40 + "\n")
                f_out.write(" -" * 40 + "\n\n")
    #             break
                
        print(f"Total student count = {student_count}\n")
        f_out.write(f"Total student count = {student_count}\n\n")

    return



if __name__ == "__main__":

    today = dt.datetime.now().strftime("%Y%m%d")

    parser = ap.ArgumentParser(description="Reads fixed width, AP Test Scores file and writes file listing students and their test scores.")
    parser.add_argument("input_filename", type=str, help="the name of the input file to be read")

    args = parser.parse_args()
    input_filename = args.input_filename

    data_file = pathlib.Path(input_filename) 
    output_file = pathlib.Path(f"AP_TestScores_{today}.txt")

    write_ap_scores(data_file, output_file)

    print(f"Output file: {output_file}")
