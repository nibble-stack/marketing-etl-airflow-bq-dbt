# tests/test_dag.py

from airflow.models import DagBag


def test_dag_import():
    dag_bag = DagBag()
    assert len(dag_bag.import_errors) == 0


def test_dag_structure():
    dag_bag = DagBag()
    dag = dag_bag.get_dag("marketing_etl")

    assert dag is not None
    assert set([t.task_id for t in dag.tasks]) == {
        "extract_marketing_data",
        "load_raw_bigquery",
        "run_dbt_models",
    }


def test_task_dependencies():
    dag_bag = DagBag()
    dag = dag_bag.get_dag("marketing_etl")

    extract = dag.get_task("extract_marketing_data")
    load = dag.get_task("load_raw_bigquery")
    dbt = dag.get_task("run_dbt_models")

    assert extract.downstream_list == [load]
    assert load.downstream_list == [dbt]
