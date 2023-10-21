import requests
import pandas as pd
import glob
import json


BASE_URL = "https://api.automait.ai/"


class Client:
    _login = None
    _password = None
    _token = None

    def __init__(self, login, password):
        self._login = login
        self._password = password
        self._check_creds()

    @property
    def login(self):
        return self._login

    @property
    def password(self):
        return self._password

    def _check_creds(self):
        payload = {"email": self._login, "password": self._password}
        r = requests.post(url=BASE_URL + "auth/", data=payload)

        print(r)
        if r.status_code == 200:
            token = r.json()["access_token"]
            self._token = f"Bearer {token}"
            return True
        else:
            raise Exception("Invalid credentials.")

    def load_multiple_csvs(self, filepath):
        filepath = filepath + "*.csv"
        filepathes = glob.glob(filepath)
        return filepathes

    def prepare_data(self, data):
        data_dict = data.to_dict("records")
        lines = 800
        splitted_data = [
            data_dict[i : i + lines] for i in range(0, len(data_dict), lines)
        ]
        return splitted_data

    def upload_lines(self, data, table_id):
        lines = json.dumps(data)
        lines = requests.post(
            url=BASE_URL + "lines/",
            json={"table_id": table_id, "lines": lines},
            headers={"Authorization": self._token},
        )
        return lines

    def add_columns_to_table(self, table_id, data):
        data_types = data.dtypes.astype(str).to_dict()
        for name, data_type in data_types.items():
            column_result = requests.post(
                url=BASE_URL + "algos/",
                json={
                    "algo": "DBColumn",
                    "out_dtype": data_type,
                    "config": json.dumps({"table_id": table_id, "column_name": name}),
                },
                headers={"Authorization": self._token},
            )
            if column_result.status_code == 201:
                continue
            else:
                raise Exception(column_result.status_code)

        return column_result

    def dataset_from_csv(
        self, name, database, host, port, ssl, username, password, filepath, primary_key
    ):
        """Add new datasets to your account by filepath or by csv.

        New datasets can be passed as a filepath to your csv file.

        Args:
            name (str): name of the dataset
            filepath (str): filepath to be used
            primary_key (str):  a column that uniquely identifies each row from your dataset
            database (str): database name or IP to connect to
            host (str): specific host name on which the DataBase is running
            port (str):  TCP port of the DataBase server is listenint to
            ssl (str): SSL-Mode to encrypt client/server communications for increased security
            username (str): your personal DataBase username
            password (str): your personal DataBase password

        Raises:
            Exception: In case an invalid filepath is passed.

        Returns:
            identifier (int): the id of your new dataset

        Examples:
            name: "diabetes"
            filepath: "files/diabetes.xlsx"
            primary_key: "patient ID"
            database: "postgres"
            host: "localhost"
            port: "5432"
            ssl: "prefer"
            username: "Max Mustermann"
            password: "123456"
        """
        try:
            data = pd.read_csv(filepath)
            dataset_id = self.add_dataset(name)[1]
        except Exception as e:
            print(e)
            raise e

        table_result = self.add_table_to_dataset(
            dataset_id, primary_key, database, host, port, ssl, username, password
        )

        self.add_columns_to_table(table_result["identifier"], data)

        try:
            splitted_data = self.prepare_data(data)

            for data in splitted_data:
                lines_result = self.upload_lines(data, table_result["identifier"])
                if lines_result.status_code == 201:
                    continue
                else:
                    raise Exception(lines_result.status_code)

            table_result = requests.put(
                url=BASE_URL + "tables/",
                json={
                    "identifier": table_result["identifier"],
                    "is_uploaded": True,
                },
                headers={"Authorization": self._token},
            )

        except Exception as e:
            print(e)
            raise e

        if table_result.status_code == 200:
            return dataset_id
        else:
            raise Exception(table_result.status_code)

    def dataset_from_xlsx(
        self, name, database, host, port, ssl, username, password, filepath, primary_key
    ):
        """Add new datasets to your account.

        New datasets can be passed as a filepath to your xlsx file.

        Args:
            name (str): name of the dataset
            filepath (str): filepath to be used
            primary_key (str):  a column that uniquely identifies each row from your dataset
            database (str): database name or IP to connect to
            host (str): specific host name on which the DataBase is running
            port (str):  TCP port of the DataBase server is listenint to
            ssl (str): SSL-Mode to encrypt client/server communications for increased security
            username (str): your personal DataBase username
            password (str): your personal DataBase password

        Raises:
            Exception: In case an invalid filepath is passed.

        Returns:
            identifier (int): the id of your new dataset

        Examples:
            name: "diabetes"
            filepath: "files/diabetes.xlsx"
            primary_key: "patient ID"
            database: "postgres"
            host: "localhost"
            port: "5432"
            ssl: "prefer"
            username: "Max Mustermann"
            password: "123456"
        """
        try:
            data = pd.read_excel(filepath)
            dataset_id = self.add_dataset(name)[1]
        except Exception as e:
            print(e)
            raise e

        table_result = self.add_table_to_dataset(
            dataset_id, primary_key, database, host, port, ssl, username, password
        )

        self.add_columns_to_table(table_result["identifier"], data)

        try:
            splitted_data = self.prepare_data(data)

            for data in splitted_data:
                uploaded_lines = self.upload_lines(data, table_result["identifier"])
                if uploaded_lines.status_code == 201:
                    continue
                else:
                    raise Exception(uploaded_lines.status_code)

            table_result = requests.put(
                url=BASE_URL + "tables/",
                json={
                    "identifier": table_result["identifier"],
                    "is_uploaded": True,
                },
                headers={"Authorization": self._token},
            )
        except Exception as e:
            print(e)
            raise e

        if table_result.status_code == 200:
            return dataset_id
        else:
            raise Exception(table_result.status_code)

    def add_table_to_dataset(
        self, dataset_id, primary_key, database, host, port, ssl, username, password
    ):
        try:
            table_result = requests.post(
                url=BASE_URL + "tables/",
                json={
                    "dataset_id": dataset_id,
                    "primary_key": primary_key,
                    "database": database,
                    "host": host,
                    "port": port,
                    "ssl": ssl,
                    "username": username,
                    "password": password,
                },
                headers={
                    "Authorization": self._token,
                },
            )
            if table_result.status_code == 201:
                requests.put(
                    url=BASE_URL + "datasets/",
                    json={
                        "identifier": dataset_id,
                        "table_ids": table_result.json()["identifier"],
                    },
                    headers={"Authorization": self._token},
                )
            else:
                raise Exception(table_result.status_code)

        except Exception as e:
            raise e

        return table_result.json()

    def get_tables(self, **condition):
        table_result = requests.get(
            url=BASE_URL + "tables/",
            params=condition,
            headers={"Authorization": self._token},
        )
        if table_result.status_code == 200:
            return table_result.json()
        else:
            raise Exception(table_result.status_code)

    def get_algos(self, **condition):
        algo_result = requests.get(
            url=BASE_URL + "algos/",
            params=condition,
            headers={"Authorization": self._token},
        )
        if algo_result.status_code == 200:
            return algo_result.json()
        else:
            raise Exception(algo_result.status_code)

    def get_dataset(self, **condition):
        dataset_result = requests.get(
            url=BASE_URL + "datasets/",
            params=condition,
            headers={"Authorization": self._token},
        )
        if dataset_result.status_code == 200:
            return dataset_result.json()
        else:
            raise Exception(dataset_result.status_code)

    def add_dataset(self, name):
        r = requests.post(
            url=BASE_URL + "datasets/",
            json={"name": name},
            headers={"Authorization": self._token},
        )
        print(r)
        if r.status_code == 201:
            data = r.json()
            return True, data["identifier"]
        else:
            raise Exception("Invalid credentials.")

    def add_model_to_dataset(self, dataset_id, task, input_col_ids, output_col_ids):
        """Add new models to your dataset.

        Args:
            dataset_id (int): identifier of the respective dataset
            task (str): machine learning task type
            input_col_ids list(int): algo ids from your dataset that are used as input for your model
            output_col_ids list(int): algo ids from your dataset that are used as target for your model

        Raises:
            Exception: In case an invalid task name is passed.

        Returns:
            identifier (int): the id of your new model
        """
        if task == "classification":
            measure = "f1"
        elif task == "regression":
            measure = "MSE"
        else:
            print(
                "Please check your submitted task. Allowed values are classification and regression"
            )
            raise AttributeError

        model_result = requests.post(
            url=BASE_URL + "table_models/",
            json={
                "dataset_id": dataset_id,
            },
            headers={"Authorization": self._token},
        )
        if model_result.status_code != 201:
            raise Exception(model_result.status_code)

        identifier = model_result.json()["identifier"]
        updated_model = requests.put(
            url=BASE_URL + "table_models/",
            json={
                "identifier": identifier,
                "dataset_id": dataset_id,
                "task": task,
                "supervised": True,
                "measure": measure,
                "status": "new",
                "input_col_ids": input_col_ids,
                "output_col_ids": output_col_ids,
            },
            headers={"Authorization": self._token},
        )
        if updated_model.status_code == 200:
            return identifier
        else:
            raise Exception(updated_model.status_code)

    def get_model(self, **condition):
        model_result = requests.get(
            url=BASE_URL + "table_models/",
            params=condition,
            headers={"Authorization": self._token},
        )
        if model_result.status_code == 200:
            return model_result.json()
        else:
            raise Exception(model_result.status_code)
