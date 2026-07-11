# _sources — PDFs de fontes primárias (fora do git)

> Os PDFs ficam locais (não versionados — ver `.gitignore`) para não inflar o repo. Este README registra URL de origem + SHA-256 para reobtenção e verificação de integridade. Entradas bibliográficas completas: `../04_SOURCE_LEDGER.md`.

| Arquivo | Fonte (URL) | SHA-256 | Ledger |
|---|---|---|---|
| cook-clay-pvsnp-official.pdf | claymath.org/wp-content/uploads/2022/06/pvsnp.pdf | `018f3d473d16c35e807e8cdfbd0bed3ccf7a56452e3e10c6b1d84b56eaf2cf59` | SRC-0003 |
| cook1971-stoc-authorcopy-scan.pdf | cs.toronto.edu/~sacook/homepage/1971.pdf (homepage do autor; scan sem camada de texto) | `aacaca0dd6db8b409317a2de282734539c3186a72cff1cb4dd601c76a4ddfb75` | SRC-0005 |
| cook1971-text-retyped.pdf | inf.unibz.it/~calvanese/teaching/14-15-tc/material/cook-1971-NP-completeness-of-SAT.pdf (redigitação com texto pesquisável) | `ae8106af2eae3d5b753e8321c8a0d57e2b68475f4b963268b87bc2387b766df2` | SRC-0005 |
| karp1972-springer2010-reprint.pdf | cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf (reprint Springer 2010 c/ introdução nova de Karp) | `ae57cf641ae4f1924bdc4d7ef865edb2411c44e3040e8e546d01f1545e288e89` | SRC-0006 |
| karp1972-uoa-scan.pdf | cgi.di.uoa.gr/~sgk/teaching/grad/handouts/karp.pdf (scan do original Plenum 1972) | `778c8b3507620a68154bc74b29810e0de6d2c4dd7ee5d24b84c7e7ba61404b81` | SRC-0006 |
| trakhtenbrot1984-perebor-survey.pdf | drdoane.com/wp-content/uploads/2020/08/survey_of_russian_approaches_to_perebor.pdf | `6b15ddd4592cd540059812191d5665bd9bccc0cbd70ff30c628699b0fabfc668` | SRC-0007 / SRC-0008 |
| arora-barak-2007-draft.pdf | theory.cs.princeton.edu/complexity/book.pdf (draft oficial do livro) | `da0881782a35bde6a0779a2eb1a8d480f39fbddf70bbb92824d1dc5550a033b2` | SRC-0010 |
| karplipton-waterloo-lecture6-secondary.pdf | cs.uwaterloo.ca/~r5olivei/courses/2022-fall-cs860/lecture06.pdf (secundária) | `78e7f7ad8d06ff34280a03de82b750893659f56b17aec1522f65c769b42c9edd` | SRC-0013 |
| razborov-rudich-1997-natural-proofs-jcss.pdf | mit6875.github.io/PAPERS/natural_proofs.pdf (versão JCSS 1997) | `5866e265ab9aa1fb10fe4d9b41009c81d95dc0d4dc0cc073539f5775a7eb81dc` | SRC-0015 |
| aaronson-wigderson-algebrization.pdf | scottaaronson.com/papers/alg.pdf (cópia do autor) | `2684e39962163da6bcfb9d17f2f49986b031f29d81a7fa5ac063d95454c3a856` | SRC-0016 |
| fortnow-relativization-survey.pdf | lance.fortnow.com/papers/files/relative.pdf | `691c660b69e46f0c0e2f51dc9cedd32ceffb46f1bad8d8866f37242bb38f7949` | SRC-0017 |
| krinkin_2026_unit_gap.pdf | arxiv.org/pdf/2603.08033 (v2, 19 Mar 2026) | `245cb67c5304a21435e5422fb14d0133ec1fdd7ba2e1eb8105cb48d9f6ab183f` | SRC-0032 |

Verificar integridade: `shasum -a 256 -c` contra os hashes acima.
