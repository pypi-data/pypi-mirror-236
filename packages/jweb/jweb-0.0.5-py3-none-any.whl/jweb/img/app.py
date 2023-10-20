import os
import re

import markdown2
import typer
from flask import Flask, jsonify, render_template, send_from_directory

from ..utils.files import get_image_files

typer_app = typer.Typer()


@typer_app.command()
def ls(  # pylint: disable=invalid-name
    path: str = typer.Argument(
        os.getcwd(), help="Path to the folder containing images.", show_default=True
    ),
    port: int = typer.Option(5000, help="Port to run the app on."),
    mkfp: str = typer.Option(
        "README.md", help="Markdown file path display the content"
    ),
    debug: bool = typer.Option(False, help="Run in debug mode."),
):
    """List images in a folder."""
    image_folder = path
    template_folder = os.path.join(os.path.dirname(__file__), "templates")
    app = Flask(
        "image list",
        static_folder=image_folder,
        static_url_path="",
        template_folder=template_folder,
    )

    @app.route("/")
    def index():
        markdown_content = ""
        if mkfp and os.path.exists(mkfp):
            with open(mkfp, "r", encoding="utf-8") as markdown_file:
                markdown_content = markdown_file.read()

        # Convert the Markdown to HTML using markdown2.
        html_content = markdown2.markdown(markdown_content)

        return render_template(
            "folder.html", html_content=html_content, title=image_folder
        )

    @app.route("/list_images/", defaults={"regex": None})
    @app.route("/list_images/<string:regex>")
    def list_images(regex):
        all_files = get_image_files(image_folder)

        if regex:  # Only apply regex if it is not None or an empty string
            try:
                filtered_files = [f for f in all_files if re.search(regex, f)]
            except re.error:
                return jsonify({"error": f"Invalid regex: {regex}"}), 400
        else:
            filtered_files = all_files  # If regex is None or empty, list all files

        return jsonify({"files": filtered_files})

    app.run(debug=debug, port=port, host="0.0.0.0")


@typer_app.command()
def diff(
    fp1: str = typer.Argument(
        os.getcwd(),
        help="Path to the first folder containing images.",
        show_default=True,
    ),
    fp2: str = typer.Argument(
        os.getcwd(),
        help="Path to the second folder containing images.",
        show_default=True,
    ),
    mkfp: str = typer.Option(
        "README.md", help="Markdown file path display the content"
    ),
    port: int = typer.Option(5000, help="Port to run the app on."),
    debug: bool = typer.Option(False, help="Run in debug mode."),
):
    """Compare images in two folders side by side."""
    left_image_folder = fp1
    right_image_folder = fp2
    print(left_image_folder, right_image_folder)
    template_folder = os.path.join(os.path.dirname(__file__), "templates")
    app = Flask("image diff", static_url_path="", template_folder=template_folder)

    @app.route("/")
    def index():
        markdown_content = ""
        if mkfp and os.path.exists(mkfp):
            with open(mkfp, "r", encoding="utf-8") as markdown_file:
                markdown_content = markdown_file.read()

        # Convert the Markdown to HTML using markdown2.
        html_content = markdown2.markdown(markdown_content)

        return render_template(
            "2side_comp.html",
            html_content=html_content,
            left_title=left_image_folder,
            right_title=right_image_folder,
        )

    @app.route("/list_images/<string:side>/", defaults={"regex": None})
    @app.route("/list_images/<string:side>/<string:regex>")
    def list_images(side, regex):
        image_folder = left_image_folder if side == "left" else right_image_folder
        all_files = get_image_files(image_folder)

        if regex:  # Only apply regex if it is not None or an empty string
            try:
                filtered_files = [f for f in all_files if re.search(regex, f)]
            except re.error:
                return jsonify({"error": "Invalid regex"}), 400
        else:
            filtered_files = all_files  # If regex is None or empty, list all files

        return jsonify({"files": filtered_files})

    @app.route("/images/<string:side>/<path:filename>")
    def serve_image(side, filename):
        image_folder = left_image_folder if side == "left" else right_image_folder
        print(side, filename, image_folder)
        return send_from_directory(image_folder, filename)

    app.run(debug=debug, port=port, host="0.0.0.0")


def main():
    typer_app()


if __name__ == "__main__":
    main()
