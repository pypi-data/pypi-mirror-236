from typing import Dict, List
import os

from parser.const import *
from genomics.variant import Variant


class VCF(Variant):
    def create_vcf_header(self, sample_id: str) -> str:
        meta = '##fileformat=VCFv4.3\n' \
               '##fileDate=20090805\n' \
               '##source=myImputationProgramV3.1\n' \
               '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n' \
               f'##reference=file://{self.ref_fa_path}\n'
        content = 'CHROM\t' \
                  'POS\t' \
                  'ID\t' \
                  'REF\t' \
                  'ALT\t' \
                  'QUAL\t' \
                  'FILTER\t' \
                  'INFO\t' \
                  'FORMAT\t' \
                  f'{sample_id}'

        return meta + content

    def to_vcf(
            self,
            company: str,
            sample_id: str,
            variant_info: List[Dict[str, List[str]]],
            output_dir: str) -> List[Dict[str, str]]:
        header = self.create_vcf_header(sample_id)
        vcf = []
        for info in variant_info:
            transcript_id = self.to_str(info[VARIANT_ACCESSION])
            cdna = self.normalize_cdna(''.join(info.get(VARIANT_HGVS, [''])))
            locus = self.to_str(info.get(VARIANT_POSITION, ['.']))
            af_str = info[VARIANT_ALLELE_FRACTION] if VARIANT_ALLELE_FRACTION in info else info[
                VARIANT_ALLELE_FREQUENCY]
            af = self.normalize_allele_freq(self.to_str(af_str))
            chrom, start, ref, alt = self.parse_hgvs_name(transcript_id, cdna, locus)
            v = {
                'CHROM': self.normalize_chrom(self.to_str(info.get(CHROMOSOME, [chrom]))),
                'POS': start,
                'ID': '.',
                'REF': ref,
                'ALT': alt,
                'QUAL': '.',
                'FILTER': '.',
                'INFO': f'AF_{company}={af}',
                'FORMAT': 'GT',
                f'{sample_id}': './.'
            }
            vcf.append(v)

        with open(os.path.join(output_dir, sample_id + '.vcf'), "w") as fp:
            fp.write(header + '\n')
            for v in vcf:
                s = map(lambda i: str(i) if type(i) is int else i, v.values())
                fp.write('\t'.join(s) + '\n')

        return vcf
