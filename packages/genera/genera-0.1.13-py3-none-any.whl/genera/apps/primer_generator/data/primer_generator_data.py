import genera
from Bio import Seq, SeqIO
from Bio.Seq import Seq
import pandas as pd
import os
import numpy as np


class PrimerGeneratorData(genera.classes.Data):
    def __init__(self, settings={}):
        super().__init__()
        self.settings = genera.utils.settings.merge(
            [genera.utils.settings.load(__file__, "data.json"), settings]
        )
        self.fragments = None
        self.primers = None
        self.fragments_file_path = None
        self.primers_file_path = None

    def load_fragments(self, file_path=None):
        if file_path is None:
            file_path = self.fragments_file_path
        self.fragments = []
        for record in SeqIO.parse(file_path, "fasta"):
            self.fragments.append(record.seq)

    def add_primers(self, primers):
        if self.primers is None:
            self.primers = []
        self.primers.append(primers)

    def reset_primers(self):
        self.primers = None

    def write_primer_xlsx(self, file_path=None):
        if file_path is None:
            file_path = self.primers_file_path

        if os.path.exists(file_path):
            os.remove(file_path)

        rows = []
        for i, df in enumerate(self.primers):
            if df.empty:
                # Create a Series of NaNs with the same columns as the first DataFrame in self.primers
                rows.append(
                    pd.Series(
                        [np.nan] * len(self.primers[0].columns),
                        index=self.primers[0].columns,
                        name=f"DF{i}",
                    )
                )
            else:
                rows.append(df.iloc[0].rename(f"DF{i}"))
        summary_df = pd.concat(rows, axis=1).T.reset_index(drop=True)

        with pd.ExcelWriter(file_path) as writer:
            summary_df.insert(
                loc=0, column="Fragment", value=range(1, len(summary_df) + 1)
            )
            summary_df.to_excel(writer, sheet_name=f"Best primers", index=False)

            for i in range(len(self.primers)):
                self.primers[i].to_excel(
                    writer, sheet_name=f"Fragment {i+1}", index=False
                )

    def list_to_seq(self, fragments):
        self.fragments = [Seq(seq) for seq in fragments]
