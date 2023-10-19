## CO2e Emission Coefficients for the Brazilian Economy

For each Brazilian economic sector and household, the CO2e emissions were estimated. This code uses this data to estimate the direct emission coefficients for each of these sectors, that is, the volume of emissions in Gg per volume produced (aggregate value in millions of reais).

In addition to the direct coefficient, the indirect emission coefficient was also estimated. The methodology for estimation is the one presented by Luis Masa in paper 'AN ESTIMATION OF THE CARBON FOOTPRINT IN SPANISH CREDIT INSTITUTIONS’ BUSINES LENDING PORTFOLIO' [here](https://repositorio.bde.es/bitstream/123456789/29610/4/do2220e.pdf).



Finally, a column named ‘sum_carteira_ativa’ was added to the final data. This represents the volume of credit taken by the sector + household and will be used in the future to create financial indicators for climate risk.

```python
!pip install sirene
from sirene import srn2 as srn
coef67_t = srn.coef('2019', lulucf = False).result
```

## Reading the Raw Emission Data (MCTI/SIRENE)

Emission data is available for 3 different gases ('CO2', 'CH4', 'N2O'). If preferred, it is also possible to consult equivalent emissions ('CO2e_GWP_SAR', 'CO2e_GWP_AR5', 'CO2e_GTP_AR5'). The available sectors are: 'agropecuaria', 'energia', 'ippu', 'lulucf', 'residuos' and 'total-brasil-1'.

```python
res_m = srn2.read('residuos','CO2')
```

