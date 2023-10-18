#!python3


def main():
    import argparse
    import os
    import platform
    from pathlib import Path

    import colour.utilities
    from matplotlib import pyplot as plt

    from colour_workbench.ETC_reports import (
        analyse_measurements_from_file,
        generate_report_page,
    )
    from colour_workbench.ETC_reports.analysis import ReflectanceData
    from colour_workbench.utilities import get_valid_filename

    colour.utilities.suppress_warnings(True)

    program_description = """
    Create the ETC LED Evaluation Report for a particular measurement file. 
    """
    parser = argparse.ArgumentParser(
        prog="ETC Display Measurements", description=program_description
    )

    parser.add_argument("file", help="The input file.")

    parser.add_argument(
        "-o",
        "--out",
        help="The output file name. Will be appended to .pdf if the file extension is excluded. If the output is a directory, the file name will be determined by the contents of the measurements.",
        default=None,
    )

    parser.add_argument(
        "--rf_45_0",
        help="45:0 reflectance factor (not as percentage)",
        default=None,
    )

    parser.add_argument(
        "--rf_45_45",
        help="45:-45 reflectance factor (not as percentage)",
        default=None,
    )

    parser.add_argument(
        "--open", action="store_true", help="Open the file after generating."
    )

    args = parser.parse_args()

    # Check File
    in_file = Path(args.file)
    if not in_file.exists() or not in_file.is_file():
        raise FileNotFoundError()

    # Analyze data
    data = analyse_measurements_from_file(str(in_file))
    reflectance = (
        ReflectanceData(reflectance_45_0=args.rf_45_0, reflectance_45_45=args.rf_45_45)
        if (args.rf_45_0 is not None and args.rf_45_45 is not None)
        else None
    )

    # Determine output file name
    if args.out is None:
        out_file_name = Path(in_file.parent)
    else:
        out_file_name = Path(args.out)
        if not out_file_name.is_file() and not out_file_name.exists():
            out_file_name.mkdir(parents=True, exist_ok=True)

    if out_file_name.is_dir():
        out_file_name = out_file_name.joinpath(get_valid_filename(data.shortname))

    out_file_name = out_file_name.with_suffix(".pdf")

    fig = generate_report_page(color_data=data, reflectance_data=reflectance)

    fig.savefig(str(out_file_name), facecolor=[1, 1, 1])

    plt.close(fig)
    if args.open:
        if platform.system() == "Windows":
            os.startfile(str(out_file_name))  # type: ignore
        else:
            os.system(f"open '{str(out_file_name)}'")
    pass


if __name__ != "__main__":
    main()
