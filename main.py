from GetResources import GetResources


def main():
    get_resources = GetResources()
    data = get_resources.create_dataframe()

    data.to_csv("salarys", sep="\t", encoding="utf-8", index=False)


if __name__ == "__main__":
    main()
