import os
import re
import numpy as np


class ElectronConfig:
    def __init__(self) -> None:
        self._import_electron_config()

    def _import_electron_config(self):
        """
        Imports electron configuration from file. Each electron configuration
        is stored as an attribute of the class. The attribute name is ec1,
        ec2, ec3, etc. The attribute value is the electron configuration
        as a string.
        """
        data_dir = os.path.join(os.path.dirname(__file__), "configurations")
        data_path = os.path.join(data_dir, "electron_configuration.txt")
        with open(data_path) as f:
            lines = f.readlines()
            lines = [l.replace("\n", "") for l in lines]

        for i, l in enumerate(lines):
            setattr(self, f"ec{i+1}", l)

    def _ec_from_nr(self, periodic_number: int) -> str:
        return getattr(self, f"ec{periodic_number}")

    def _split_ec_in_row(self, periodic_number: int) -> np.ndarray:
        """
        Splits electron configuration into rows. Each row is a numpy array
        with three elements. The first element is the shell number, the second
        element is the subshell letter and the third element is the number of
        electrons in the subshell.

        Args:
            periodic_number (int): The periodic number of the element.

        Returns:
            np.ndarray: numpy array with three elements for each row.
        """
        ec_rowsplit = np.array(  # regex to split string into numbers and letters
            re.findall("\d+|\D+", self._ec_from_nr(periodic_number)) + [" "],
            dtype="object",
        ).reshape(-1, 4)[:, :3]
        ec_rowsplit[:, 0] = list(map(int, ec_rowsplit[:, 0]))  # convert to int
        ec_rowsplit[:, 2] = list(map(int, ec_rowsplit[:, 2]))  # convert to int
        return ec_rowsplit

    def _row_arr_to_str(self, row: np.ndarray) -> str:
        """
        Converts an array on the form from _split_ec_in_row to a string.

        Args:
            row (np.ndarray): numpy array with three elements for each row.

        Returns:
            str: string with electron configuration.
        """
        row[:, 0] = list(map(str, row[:, 0]))
        row[:, 2] = list(map(str, row[:, 2]))
        row_list = list(map("".join, row))
        return " ".join(row_list)

    def remove_electrons(self, periodic_number: int, remove_ec: int) -> str:
        """
        Removes electrons from the electron configuration and returns the
        new electron configuration as a string.

        Args:
            periodic_number (int): The periodic number of the element.
            remove_ec (int): The number of electrons to remove.

        Returns:
            str: The new electron configuration as a string.
        """
        if periodic_number == remove_ec:
            return ""
        elif periodic_number < remove_ec:
            raise ValueError(
                "You can not remove more electrons than the element has."
                "Hence periodic_number must be greater than remove_ec."
            )

        ec_rowsplit = self._split_ec_in_row(periodic_number)
        electrons = ec_rowsplit[:, 2]
        ec_reverse_cumsum = np.cumsum(electrons[::-1])

        for i, sum_ in enumerate(ec_reverse_cumsum):
            if sum_ == remove_ec:
                ec_reduced = ec_rowsplit[: len(ec_rowsplit) - (i + 1)]
                break
            elif sum_ > remove_ec:
                last_electron = sum_ - remove_ec
                ec_reduced = ec_rowsplit[: len(ec_rowsplit) - i]
                ec_reduced[-1, -1] = last_electron
                break

        return self._row_arr_to_str(ec_reduced)

    def n0(self, periodic_number: int, remove_ec: int) -> int:
        """
        Finds the principle quantum number of outermost projectile electron.
        Example1:
        Consider mg with 12 electrons. The electron configuration is
        1s2 2s2 2p6 3s2. If we remove 7 electrons we get 1s2 2s2 2p1.
        Hence n0 = 2 because the outermost electron is in the second shell.

        Example2:
        Consider O with 8 electrons. The electron configuration is
        1s2 2s2 2p4. If we remove 6 electrons we get 1s2.
        Hence n0 = 1 because the outermost electron is in the first shell.

        Args:
            periodic_number (int): The periodic number of the element.
            remove_ec (int): The number of electrons to remove.

        Returns:
            int: The principle quantum number of the outermost projectile
            electron.
        """
        if periodic_number == remove_ec:
            raise ValueError(
                "It is not possible to find n0 for an element with no electrons."
            )
        elif periodic_number < remove_ec:
            raise ValueError(
                "You can not remove more electrons than the element has."
                "Hence periodic_number must be greater than remove_ec."
            )
        reduced_ec = self.remove_electrons(periodic_number, remove_ec)
        return int(re.findall("\d+|\D+", reduced_ec)[-3])
