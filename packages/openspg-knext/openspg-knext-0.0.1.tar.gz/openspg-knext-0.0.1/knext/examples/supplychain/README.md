
```shell
knext project create --prj_path .
```
```
knext schema commit
```
knext builder submit TaxOfCompanyEvent
knext builder submit TaxOfProdEvent
knext schema reg_concept_rule --file ./schema/concept.rule

knext operator publish CompanyLinkerOperator

knext builder submit Index,Trend
knext builder submit Industry,Product,ProductHasSupplyChain
knext builder submit Company,CompanyFundTrans
knext builder submit Person
knext builder submit ProductChainEvent

knext reasoner query --dsl "MATCH (s:SupplyChain.Company) RETURN s.id,s.name,s.totalTransInAmt"
knext reasoner query --dsl "MATCH (s:SupplyChain.Company)-[:mainSupply]->(o:SupplyChain.Company) RETURN s.id,s.name,o.id,o.name"
knext reasoner query --dsl "MATCH (s:SupplyChain.Company)-[p:belongToIndustry]->(o:SupplyChain.Industry) RETURN s.id,s.name,o.id"
knext reasoner query --dsl "MATCH (s:SupplyChain.Company) RETURN s.name,s.fundTrans3Month"
knext reasoner query --dsl "MATCH (s:SupplyChain.Company) RETURN s.name,s.fundTrans1Month"
knext reasoner query --file ./reasoner/same_legal_reprensentative.dsl
knext reasoner query --file ./reasoner/fund_trans_feature.dsl

