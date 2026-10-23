
from pathlib import Path

import pandas as pd
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Employee Analytics")

DATA_FILE = Path(__file__).parent / "data" / "employees_100.csv"


def load_data():
    """Load and validate the employee dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"CSV file not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    required = {
        "id", "first_name", "last_name",
        "email", "gender", "department", "salary"
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing CSV columns: {sorted(missing)}")

    return df


@mcp.tool()
def get_employee_summary() -> dict:
    """Get total employees, departments, average salary, and missing values."""
    df = load_data()

    return {
        "total_employees": int(len(df)),
        "total_departments": int(df["department"].nunique()),
        "average_salary": round(float(df["salary"].mean()), 2),
        "missing_values": {
            str(k): int(v)
            for k, v in df.isnull().sum().items()
        },
    }


@mcp.tool()
def get_department_stats() -> list[dict]:
    """Get employee count and average salary for each department."""
    df = load_data()

    result = (
        df.groupby("department")
        .agg(
            employee_count=("id", "count"),
            average_salary=("salary", "mean"),
            total_salary=("salary", "sum"),
        )
        .reset_index()
        .sort_values("employee_count", ascending=False)
    )

    result["average_salary"] = result["average_salary"].round(2)

    return result.to_dict(orient="records")


@mcp.tool()
def get_salary_statistics() -> dict:
    """Get overall salary count, average, median, minimum, and maximum."""
    df = load_data()
    salary = pd.to_numeric(df["salary"], errors="coerce").dropna()

    if salary.empty:
        return {"error": "No valid salary values found."}

    return {
        "employees_with_salary": int(salary.count()),
        "average_salary": round(float(salary.mean()), 2),
        "median_salary": float(salary.median()),
        "minimum_salary": float(salary.min()),
        "maximum_salary": float(salary.max()),
    }


@mcp.tool()
def get_top_paid_employees(limit: int = 5) -> list[dict]:
    """Get the highest-paid employees. Limit must be between 1 and 20."""
    if not 1 <= limit <= 20:
        return {"error": "Limit must be between 1 and 20."}

    df = load_data().nlargest(limit, "salary")

    df["full_name"] = df["first_name"] + " " + df["last_name"]

    return df[
        ["id", "full_name", "department", "salary"]
    ].to_dict(orient="records")


@mcp.tool()
def search_employees(query: str) -> list[dict]:
    """Search employees by first name, last name, email, or department."""
    if not query.strip():
        return []

    df = load_data()
    pattern = query.strip()

    mask = (
        df["first_name"].str.contains(pattern, case=False, na=False, regex=False)
        | df["last_name"].str.contains(pattern, case=False, na=False, regex=False)
        | df["email"].str.contains(pattern, case=False, na=False, regex=False)
        | df["department"].str.contains(pattern, case=False, na=False, regex=False)
    )

    result = df.loc[mask].head(50).copy()
    result["full_name"] = result["first_name"] + " " + result["last_name"]

    return result[
        ["id", "full_name", "email", "department", "salary"]
    ].to_dict(orient="records")


@mcp.tool()
def get_gender_distribution() -> dict:
    """Get the number of employees in each gender category."""
    df = load_data()
    return {
        str(gender): int(count)
        for gender, count in df["gender"].value_counts().items()
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
