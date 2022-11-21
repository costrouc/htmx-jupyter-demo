import uvicorn


def main(host="0.0.0.0", port=8000, reload=True):
    uvicorn.run(
        "htmx_jupyter.app:app",
        host=host,
        port=port,
        reload=reload,
        reload_includes=[
            "**/*.py",
            "**/*.html",
        ]
    )


if __name__ == "__main__":
    main()
