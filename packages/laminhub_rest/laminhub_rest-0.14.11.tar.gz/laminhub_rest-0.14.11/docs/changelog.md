# Changelog

<!-- prettier-ignore -->
Name | PR | Developer | Date | Version
--- | --- | --- | --- | ---
🐛 Enable admin to deploy an instance servers | [315](https://github.com/laminlabs/laminhub-rest/pull/315) | [fredericenard](https://github.com/fredericenard) | 2023-10-16 |
🔒 Update role in vault when updating a collaborator | [313](https://github.com/laminlabs/laminhub-rest/pull/313) | [fredericenard](https://github.com/fredericenard) | 2023-10-06 | 0.14.11
🔒 Delete role in vault when deleting collaborator | [312](https://github.com/laminlabs/laminhub-rest/pull/312) | [fredericenard](https://github.com/fredericenard) | 2023-10-06 | 0.14.10
🐛 Fix delete for deployed instances | [311](https://github.com/laminlabs/laminhub-rest/pull/311) | [fredericenard](https://github.com/fredericenard) | 2023-10-06 |
👔 Return deployment information in `account-instances` endpoint | [310](https://github.com/laminlabs/laminhub-rest/pull/310) | [bpenteado](https://github.com/bpenteado) | 2023-10-03 | 0.14.9
✨ Create new endpoint to fetch account instances with role | [309](https://github.com/laminlabs/laminhub-rest/pull/309) | [bpenteado](https://github.com/bpenteado) | 2023-10-03 | 0.14.8
📌 Pin lamin_vault | [308](https://github.com/laminlabs/laminhub-rest/pull/308) | [fredericenard](https://github.com/fredericenard) | 2023-10-03 | 0.14.7
🔒 Add instance_id argument to create_token_from_jwt endpoint | [307](https://github.com/laminlabs/laminhub-rest/pull/307) | [fredericenard](https://github.com/fredericenard) | 2023-10-03 | 0.14.6
✅ Add test for vault | [306](https://github.com/laminlabs/laminhub-rest/pull/306) | [fredericenard](https://github.com/fredericenard) | 2023-10-02 |
👷 Add vault credentials | [305](https://github.com/laminlabs/laminhub-rest/pull/305) | [fredericenard](https://github.com/fredericenard) | 2023-10-02 | 0.14.5
🗃️ Create unique constraint on lamin_instance_id | [304](https://github.com/laminlabs/laminhub-rest/pull/304) | [fredericenard](https://github.com/fredericenard) | 2023-09-30 | 0.14.4
🐛 Fix import | [303](https://github.com/laminlabs/laminhub-rest/pull/303) | [fredericenard](https://github.com/fredericenard) | 2023-09-30 | 0.14.3
👷 Add GH_ACCESS_TOKEN to server environment | [302](https://github.com/laminlabs/laminhub-rest/pull/302) | [fredericenard](https://github.com/fredericenard) | 2023-09-30 | 0.14.2
✨ Add cloud_run_instance_name_prefix to endpoint parameters | [301](https://github.com/laminlabs/laminhub-rest/pull/301) | [fredericenard](https://github.com/fredericenard) | 2023-09-30 | 0.14.1
🚸 Improve deploy endpoint | [299](https://github.com/laminlabs/laminhub-rest/pull/299) | [fredericenard](https://github.com/fredericenard) | 2023-09-30 | 0.14.0
✨ Add deployment endpoint | [298](https://github.com/laminlabs/laminhub-rest/pull/298) | [fredericenard](https://github.com/fredericenard) | 2023-09-30 |
♻️ Use vault logic from lamin_vault | [295](https://github.com/laminlabs/laminhub-rest/pull/295) | [fredericenard](https://github.com/fredericenard) | 2023-09-26 |
✨ Create server logic to interact with HashiCorp Vault | [294](https://github.com/laminlabs/laminhub-rest/pull/294) | [fredericenard](https://github.com/fredericenard) | 2023-09-22 |
👷 Modify workflow trigger | [293](https://github.com/laminlabs/laminhub-rest/pull/293) | [fredericenard](https://github.com/fredericenard) | 2023-09-18 |
🎨 Use context manager when creating test auth | [292](https://github.com/laminlabs/laminhub-rest/pull/292) | [bpenteado](https://github.com/bpenteado) | 2023-09-15 |
👷 Update environment variables and test auth redirect | [291](https://github.com/laminlabs/laminhub-rest/pull/291) | [bpenteado](https://github.com/bpenteado) | 2023-09-15 |
🐛 Fix redirect during `create_test_auth` | [290](https://github.com/laminlabs/laminhub-rest/pull/290) | [bpenteado](https://github.com/bpenteado) | 2023-09-15 |
🐛  Fix redirect after `create_test_auth` | [289](https://github.com/laminlabs/laminhub-rest/pull/289) | [bpenteado](https://github.com/bpenteado) | 2023-09-15 |
✅ Run integration tests | [288](https://github.com/laminlabs/laminhub-rest/pull/288) | [bpenteado](https://github.com/bpenteado) | 2023-09-15 |
♻️ Remove server extra & clean up noxfile | [287](https://github.com/laminlabs/laminhub-rest/pull/287) | [falexwolf](https://github.com/falexwolf) | 2023-09-15 |
🔥 Remove lamindb-setup | [286](https://github.com/laminlabs/laminhub-rest/pull/286) | [falexwolf](https://github.com/falexwolf) | 2023-09-15 |
 🔖 Release version 0.12.0 | [281](https://github.com/laminlabs/laminhub-rest/pull/281) | [fredericenard](https://github.com/fredericenard) | 2023-09-14 |
🚸 Do not run supabase status automatically | [263](https://github.com/laminlabs/laminhub-rest/pull/263) | [falexwolf](https://github.com/falexwolf) | 2023-09-07 |
♻️ Re-enable connector on S3 | [261](https://github.com/laminlabs/laminhub-rest/pull/261) | [falexwolf](https://github.com/falexwolf) | 2023-09-07 |
♻️ Refactor connector access: `orm` → `connector` containing all relevant aspects | [260](https://github.com/laminlabs/laminhub-rest/pull/260) | [falexwolf](https://github.com/falexwolf) | 2023-09-07 |
🔥 Delete unnecessary logic in config & rename `Settings` to `Environment` | [259](https://github.com/laminlabs/laminhub-rest/pull/259) | [falexwolf](https://github.com/falexwolf) | 2023-09-07 |
🗃️ Create AccountInstanceDBUser table | [257](https://github.com/laminlabs/laminhub-rest/pull/257) | [fredericenard](https://github.com/fredericenard) | 2023-09-06 |
⬆️ Upgrade lamindb-setup | [258](https://github.com/laminlabs/laminhub-rest/pull/258) | [falexwolf](https://github.com/falexwolf) | 2023-09-06 |
🚚 Rename `lnhub-rest` to `laminhub-rest` | [256](https://github.com/laminlabs/laminhub-rest/pull/256) | [falexwolf](https://github.com/falexwolf) | 2023-09-06 |
👷 Monitor coverage | [254](https://github.com/laminlabs/laminhub-rest/pull/254) | [falexwolf](https://github.com/falexwolf) | 2023-09-06 |
🔒 Create RLS policies for laminapp-admin | [252](https://github.com/laminlabs/laminhub-rest/pull/252) | [fredericenard](https://github.com/fredericenard) | 2023-08-31 |
👔  Return caller role in `get_instance_by_id` | [251](https://github.com/laminlabs/laminhub-rest/pull/251) | [bpenteado](https://github.com/bpenteado) | 2023-08-30 | 0.10.18
✨ Create `get_instance_by_id` router | [250](https://github.com/laminlabs/laminhub-rest/pull/250) | [bpenteado](https://github.com/bpenteado) | 2023-08-30 | 0.10.17
♻️ Refactor noxfile, only prettification, no changes | [249](https://github.com/laminlabs/laminhub-rest/pull/249) | [falexwolf](https://github.com/falexwolf) | 2023-08-19 |
✨ Create helper function to select user by id | [248](https://github.com/laminlabs/laminhub-rest/pull/248) | [bpenteado](https://github.com/bpenteado) | 2023-08-17 | 0.10.16
♻️ Update router path and arguments | [247](https://github.com/laminlabs/laminhub-rest/pull/247) | [fredericenard](https://github.com/fredericenard) | 2023-08-14 | 0.10.15
✨ Create endpoint to update last_access_at value | [246](https://github.com/laminlabs/laminhub-rest/pull/246) | [fredericenard](https://github.com/fredericenard) | 2023-08-14 | 0.10.13
🐛 Use post requests for instance linking | [245](https://github.com/laminlabs/laminhub-rest/pull/245) | [fredericenard](https://github.com/fredericenard) | 2023-08-11 | 0.10.11
✨ Create endpoint link arbitrary cloud run and lamin instances | [244](https://github.com/laminlabs/laminhub-rest/pull/244) | [fredericenard](https://github.com/fredericenard) | 2023-08-10 | 0.10.10
🔒 Use service role key to manage cloud run instances | [243](https://github.com/laminlabs/laminhub-rest/pull/243) | [fredericenard](https://github.com/fredericenard) | 2023-08-08 | 0.10.9
📝 Update migration process | [240](https://github.com/laminlabs/laminhub-rest/pull/240) | [bpenteado](https://github.com/bpenteado) | 2023-08-08 |
✨ Implement eviction mechanism and remove useless endpoints | [242](https://github.com/laminlabs/laminhub-rest/pull/242) | [fredericenard](https://github.com/fredericenard) | 2023-08-08 | 0.10.8
🐛  Add missing dotenv dependency | [239](https://github.com/laminlabs/laminhub-rest/pull/239) | [fredericenard](https://github.com/fredericenard) | 2023-08-07 | 0.10.7
✨ Add endpoint to get cloud run instance by name | [238](https://github.com/laminlabs/laminhub-rest/pull/238) | [fredericenard](https://github.com/fredericenard) | 2023-08-07 | 0.10.6
✨ Add endpoint to get cloud run instance by name | [237](https://github.com/laminlabs/laminhub-rest/pull/237) | [fredericenard](https://github.com/fredericenard) | 2023-08-07 |
🗃️ Expand `CloudRunInstance` table and RLS | [236](https://github.com/laminlabs/laminhub-rest/pull/236) | [bpenteado](https://github.com/bpenteado) | 2023-08-03 |
✨ Create endpoints to manage cloud run instances | [233](https://github.com/laminlabs/laminhub-rest/pull/233) | [fredericenard](https://github.com/fredericenard) | 2023-07-30 | 0.10.4
👔 Update add-collaborator endpoint | [232](https://github.com/laminlabs/laminhub-rest/pull/232) | [bpenteado](https://github.com/bpenteado) | 2023-07-25 | 0.10.3
⬆️  Upgrade lamindb-setup to fix flawed `init_instance` logic | [229](https://github.com/laminlabs/laminhub-rest/pull/229) | [bpenteado](https://github.com/bpenteado) | 2023-07-24 |
🗃️ Cascade delete `DBUSer` and create `CloudRunInstance` | [230](https://github.com/laminlabs/laminhub-rest/pull/230) | [bpenteado](https://github.com/bpenteado) | 2023-07-24 | 0.10.2
🗃️ Cascade delete `DBUser` and create `CloudRunInstance` | [231](https://github.com/laminlabs/laminhub-rest/pull/231) | [bpenteado](https://github.com/bpenteado) | 2023-07-21 |
🗃️ Enable multiple DB access roles in instances (decompose connection string) | [227](https://github.com/laminlabs/laminhub-rest/pull/227) | [bpenteado](https://github.com/bpenteado) | 2023-07-18 | 0.10.1
🎨 Update `add-collaborator` endpoint | [228](https://github.com/la/laminhub-rest/pull/228) | [bpenteado](https://github.com/bpenteado) | 2023-07-10 |
🗃️ Enable multiple DB access roles in instances (decompose connection string) | [226](https://github.com/laminlabs/laminhub-rest/pull/226) | [bpenteado](https://github.com/bpenteado) | 2023-07-06 |
👷 Test hub components of `lamindb_setup` locally | [225](https://github.com/laminlabs/laminhub-rest/pull/225) | [bpenteado](https://github.com/bpenteado) | 2023-06-26 |
✅ Try to add one of Lawrence's unit tests | [224](https://github.com/laminlabs/laminhub-rest/pull/224) | [falexwolf](https://github.com/falexwolf) | 2023-06-22 |
💚 Fix submodule config & upgrade lamindb-setup | [223](https://github.com/laminlabs/laminhub-rest/pull/223) | [falexwolf](https://github.com/falexwolf) | 2023-06-21 |
👷 Integrate two GA workflows | [222](https://github.com/laminlabs/laminhub-rest/pull/222) | [falexwolf](https://github.com/falexwolf) | 2023-06-21 |
🔥 Remove unused env variables | [221](https://github.com/laminlabs/laminhub-rest/pull/221) | [falexwolf](https://github.com/falexwolf) | 2023-06-21 |
🔥 Remove check_breaks_lndb | [220](https://github.com/laminlabs/laminhub-rest/pull/220) | [falexwolf](https://github.com/falexwolf) | 2023-06-21 |
🔥 Remove client functionality from laminhub-rest, it is entirely contained in lamindb-setup | [219](https://github.com/laminlabs/laminhub-rest/pull/219) | [bpenteado](https://github.com/bpenteado) | 2023-06-21 |
♻️  Standardize and document endpoints | [218](https://github.com/laminlabs/laminhub-rest/pull/218) | [bpenteado](https://github.com/bpenteado) | 2023-06-11 |
👷 Refactor DevOps | [217](https://github.com/laminlabs/laminhub-rest/pull/217) | [bpenteado](https://github.com/bpenteado) | 2023-06-08 |
🚚 Rename `lndb` to `lamindb_setup` | [216](https://github.com/laminlabs/laminhub-rest/pull/216) | [falexwolf](https://github.com/falexwolf) | 2023-06-04 | 0.9.10
🔥 Remove not-needed assets | [215](https://github.com/laminlabs/laminhub-rest/pull/215) | [falexwolf](https://github.com/falexwolf) | 2023-06-04 | 0.9.9
➖ Simplify dependencies | [208](https://github.com/laminlabs/laminhub-rest/pull/208) | [falexwolf](https://github.com/falexwolf) | 2023-05-28 | 0.9.8
➖ Replace boto3 with botocore | [206](https://github.com/laminlabs/laminhub-rest/pull/206) | [Koncopd](https://github.com/Koncopd) | 2023-05-26 |
🍱 Update assets | [207](https://github.com/laminlabs/laminhub-rest/pull/207) | [falexwolf](https://github.com/falexwolf) | 2023-05-25 |
➖ Streamline dependencies | [205](https://github.com/laminlabs/laminhub-rest/pull/205) | [bpenteado](https://github.com/bpenteado) | 2023-05-10 | 0.9.6
🔖 Staging version 0.9.5 | [199](https://github.com/laminlabs/laminhub-rest/pull/199) | [bpenteado](https://github.com/bpenteado) | 2023-05-09 | 0.9.5
👷 Fix deployment in main branch | [201](https://github.com/laminlabs/laminhub-rest/pull/201) | [lawrlee](https://github.com/lawrlee) | 2023-05-09 |
✨ Create endpoints to update and delete collaborators | [197](https://github.com/laminlabs/laminhub-rest/pull/197) | [bpenteado](https://github.com/bpenteado) | 2023-05-09 |
🍱 Register trexbio schema | [195](https://github.com/laminlabs/laminhub-rest/pull/195) | [sunnyosun](https://github.com/sunnyosun) | 2023-04-28 | 0.9.4
Remove build workflow when making a release | [193](https://github.com/laminlabs/laminhub-rest/pull/193) | [lawrlee](https://github.com/lawrlee) | 2023-04-27 |
✨ Allow local storage locations | [194](https://github.com/laminlabs/laminhub-rest/pull/194) | [falexwolf](https://github.com/falexwolf) | 2023-04-27 | 0.9.3
✨ Add `is_collaborator` endpoint | [191](https://github.com/laminlabs/laminhub-rest/pull/191) | [fredericenard](https://github.com/fredericenard) | 2023-04-25 | 0.9.2
👷 Refactor environment management  | [180](https://github.com/laminlabs/laminhub-rest/pull/180) | [lawrlee](https://github.com/lawrlee) | 2023-04-24 |
🔖 Staging version 0.9.0 | [170](https://github.com/laminlabs/laminhub-rest/pull/170) | [falexwolf](https://github.com/falexwolf) | 2023-04-24 | 0.9.1
🎨 Redesign acct-instances endpoint | [190](https://github.com/laminlabs/laminhub-rest/pull/190) | [bpenteado](https://github.com/bpenteado) | 2023-04-23 |
✨ Create add-collaborator endpoint | [189](https://github.com/laminlabs/laminhub-rest/pull/189) | [bpenteado](https://github.com/bpenteado) | 2023-04-23 |
🎨 Enrich account organizations endpoint | [188](https://github.com/laminlabs/laminhub-rest/pull/188) | [bpenteado](https://github.com/bpenteado) | 2023-04-23 |
🍱 Add schema module `lamin1` | [187](https://github.com/laminlabs/laminhub-rest/pull/187) | [falexwolf](https://github.com/falexwolf) | 2023-04-22 | 0.8.2
🚸 Ask for postgresql instead of postgres | [186](https://github.com/laminlabs/laminhub-rest/pull/186) | [falexwolf](https://github.com/falexwolf) | 2023-04-22 |
👷 Run tests on staging | [179](https://github.com/laminlabs/laminhub-rest/pull/179) | [falexwolf](https://github.com/falexwolf) | 2023-04-20 |
✅ Decouple tests from lndb-related objects | [184](https://github.com/laminlabs/laminhub-rest/pull/184) | [bpenteado](https://github.com/bpenteado) | 2023-04-20 |
💚 Fix tests | [178](https://github.com/laminlabs/laminhub-rest/pull/178) | [falexwolf](https://github.com/falexwolf) | 2023-04-18 |
🚚 Rename folders in docs | [177](https://github.com/laminlabs/laminhub-rest/pull/177) | [falexwolf](https://github.com/falexwolf) | 2023-04-18 |
🏗️ Clean up historical migrations & remove cloning from production for migrations testing | [175](https://github.com/laminlabs/laminhub-rest/pull/175) | [falexwolf](https://github.com/falexwolf) | 2023-04-18 |
🏗️ Fix local development setup | [174](https://github.com/laminlabs/laminhub-rest/pull/174) | [falexwolf](https://github.com/falexwolf) | 2023-04-18 | 0.8.1
🗃️ Fix RLS for storage table | [173](https://github.com/laminlabs/laminhub-rest/pull/173) | [fredericenard](https://github.com/fredericenard) | 2023-04-18 |
✨ Create organization endpoints | [165](https://github.com/laminlabs/laminhub-rest/pull/165) | [bpenteado](https://github.com/bpenteado) | 2023-04-17 |
👷 Run tests against `lndb` | [143](https://github.com/laminlabs/laminhub-rest/pull/143) | [falexwolf](https://github.com/falexwolf) | 2023-04-13 |
♻️ Simplify migrations testing | [168](https://github.com/laminlabs/laminhub-rest/pull/168) | [falexwolf](https://github.com/falexwolf) | 2023-04-12 |
🗃️ Create organization membership table | [163](https://github.com/laminlabs/laminhub-rest/pull/163) | [bpenteado](https://github.com/bpenteado) | 2023-04-11 |
🗃️ Reset RLS policies | [161](https://github.com/laminlabs/laminhub-rest/pull/161) | [bpenteado](https://github.com/bpenteado) | 2023-04-05 |
🗃️ Implement cascade deletion on instance table | [158](https://github.com/laminlabs/laminhub-rest/pull/158) | [bpenteado](https://github.com/bpenteado) | 2023-04-04 |
✨ Create endpoint to fetch an avatar | [167](https://github.com/laminlabs/laminhub-rest/pull/167) | [fredericenard](https://github.com/fredericenard) | 2023-04-07 |
✨ Create an endpoint to fetch avatar given a list of lnid | [166](https://github.com/laminlabs/laminhub-rest/pull/166) | [fredericenard](https://github.com/fredericenard) | 2023-04-07 | 0.7.3
🐛 Fix sign in | [160](https://github.com/laminlabs/laminhub-rest/pull/160) | [fredericenard](https://github.com/fredericenard) | 2023-03-31 | 0.7.2
🐛 Enforce compatibility with new sign in API | [159](https://github.com/laminlabs/laminhub-rest/pull/159) | [fredericenard](https://github.com/fredericenard) | 2023-03-31 | 0.7.1
🔖 Staging version 0.7.0 | [150](https://github.com/laminlabs/laminhub-rest/pull/150) | [fredericenard](https://github.com/fredericenard) | 2023-03-29 | 0.7.0
⚡ Improve instance deletion through RLS | [154](https://github.com/laminlabs/laminhub-rest/pull/154) | [bpenteado](https://github.com/bpenteado) | 2023-03-29 | 0.7rc1
✨ Enable instance ownership transfer | [156](https://github.com/laminlabs/laminhub-rest/pull/156) | [bpenteado](https://github.com/bpenteado) | 2023-03-28 |
Deploy laminhub-rest on Cloud Run using Github actions | [155](https://github.com/laminlabs/laminhub-rest/pull/155) | [lawrlee](https://github.com/lawrlee) | 2023-03-27 |
🐛 Ensure integrity of RLS for local tests | [152](https://github.com/laminlabs/laminhub-rest/pull/152) | [fredericenard](https://github.com/fredericenard) | 2023-03-24 |
🐛 Add test to ensure an owner can delete collaborators | [153](https://github.com/laminlabs/laminhub-rest/pull/153) | [fredericenard](https://github.com/fredericenard) | 2023-03-24 |
⬆️ Upgrade supabase | [149](https://github.com/laminlabs/laminhub-rest/pull/149) | [fredericenard](https://github.com/fredericenard) | 2023-03-23 |
🔖 Staging version 0.7.0 | [148](https://github.com/laminlabs/laminhub-rest/pull/148) | [bpenteado](https://github.com/bpenteado) | 2023-03-21 |
🐛 Fix collaboration deletion during instance deletion | [146](https://github.com/laminlabs/laminhub-rest/pull/146) | [bpenteado](https://github.com/bpenteado) | 2023-03-21 |
🎨  Return storage root in API fetching of instance | [144](https://github.com/laminlabs/laminhub-rest/pull/144) | [bpenteado](https://github.com/bpenteado) | 2023-03-15 |
🚑  Delete all collaborators when deleting an instance | [142](https://github.com/laminlabs/laminhub-rest/pull/142) | [bpenteado](https://github.com/bpenteado) | 2023-03-13 |
✏️ Fix typo | [140](https://github.com/laminlabs/laminhub-rest/pull/140) | [fredericenard](https://github.com/fredericenard) | 2023-03-11 |
⚡ Remove instance filter | [139](https://github.com/laminlabs/laminhub-rest/pull/139) | [fredericenard](https://github.com/fredericenard) | 2023-03-10 |
💚 Fix failing test in CI local environment | [138](https://github.com/laminlabs/laminhub-rest/pull/138) | [fredericenard](https://github.com/fredericenard) | 2023-03-10 |
🔒 Update RLS for version and migration table | [135](https://github.com/laminlabs/laminhub-rest/pull/135) | [fredericenard](https://github.com/fredericenard) | 2023-03-10 |
✅ Move check-break-lndb to ensure it runs on all environments | [136](https://github.com/laminlabs/laminhub-rest/pull/136) | [fredericenard](https://github.com/fredericenard) | 2023-03-09 |
🐛 Fix wrong condition to choose environment | [134](https://github.com/laminlabs/laminhub-rest/pull/134) | [fredericenard](https://github.com/fredericenard) | 2023-03-09 |
Disentangle dependencies | [commit](https://github.com/laminlabs/laminhub-rest/commit/46137b10ee82b26bba22349f200ca5586363dae1) | [falexwolf](https://github.com/falexwolf) | 2023-03-09 | 0.6.1
Staging version 0.6.0 | [120](https://github.com/laminlabs/laminhub-rest/pull/120) | [fredericenard](https://github.com/fredericenard) | 2023-03-08 |
✅ Update comparison between nested dictionnaries with deepdiff | [133](https://github.com/laminlabs/laminhub-rest/pull/133) | [bpenteado](https://github.com/bpenteado) | 2023-03-08 | 0.6.0
⬆️ Upgrade lndb | [132](https://github.com/laminlabs/laminhub-rest/pull/132) | [fredericenard](https://github.com/fredericenard) | 2023-03-07 | 0.5.2
🔒 Prevent using boto3 through the REST API | [131](https://github.com/laminlabs/laminhub-rest/pull/131) | [fredericenard](https://github.com/fredericenard) | 2023-03-07 |
👷 Move branch environment logic in nox file | [130](https://github.com/laminlabs/laminhub-rest/pull/130) | [fredericenard](https://github.com/fredericenard) | 2023-03-07 |
📝 Clean up test assets in notebooks | [129](https://github.com/laminlabs/laminhub-rest/pull/129) | [bpenteado](https://github.com/bpenteado) | 2023-03-07 |
👷 Clean up CI accounts | [128](https://github.com/laminlabs/laminhub-rest/pull/128) | [fredericenard](https://github.com/fredericenard) | 2023-03-05 |
👷 Latest changes workflow | [127](https://github.com/laminlabs/laminhub-rest/pull/127) | [fredericenard](https://github.com/fredericenard) | 2023-03-04 | 0.6.0rc1
🚑 Fix trailing slash for storage root | [109](https://github.com/laminlabs/laminhub-rest/pull/109) | [falexwolf](https://github.com/falexwolf) | 2023-02-22 | 0.5.1
✨ Enable REST to understand auth | [105](https://github.com/laminlabs/laminhub-rest/pull/105) | [fredericenard](https://github.com/fredericenard) | 2023-02-21 | 0.5.0
✨ Enable test on local Supabase | [104](https://github.com/laminlabs/laminhub-rest/pull/104) | [fredericenard](https://github.com/fredericenard) | 2023-02-21 |
💚 Fix cleaning of accounts created by CI | [103](https://github.com/laminlabs/laminhub-rest/pull/103) | [fredericenard](https://github.com/fredericenard) | 2023-02-18 |
:children_crossing: Better db arg validation | [101](https://github.com/laminlabs/laminhub-rest/pull/101) | [falexwolf](https://github.com/falexwolf) | 2023-02-17 |
✨ Use access token to delete instance | [100](https://github.com/laminlabs/laminhub-rest/pull/100) | [fredericenard](https://github.com/fredericenard) | 2023-02-17 |
✨ Use access token to create instance | [99](https://github.com/laminlabs/laminhub-rest/pull/99) | [fredericenard](https://github.com/fredericenard) | 2023-02-17 |
🐛 Fix permission not defined | [98](https://github.com/laminlabs/laminhub-rest/pull/98) | [fredericenard](https://github.com/fredericenard) | 2023-02-17 |
✨ Add routes to retrieve instance metadata | [87](https://github.com/laminlabs/laminhub-rest/pull/87) | [fredericenard](https://github.com/fredericenard) | 2023-02-17 |
📝 Add notes folder with signup note | [97](https://github.com/laminlabs/laminhub-rest/pull/97) | [falexwolf](https://github.com/falexwolf) | 2023-02-16 |
🎨 Check `breaks_lndb` internally in `laminhub_rest` for functions used in `lndb` | [96](https://github.com/laminlabs/laminhub-rest/pull/96) | [falexwolf](https://github.com/falexwolf) | 2023-02-16 | 0.4.3
🚸 Less strict check on whether hub breaks lndb | [95](https://github.com/laminlabs/laminhub-rest/pull/95) | [falexwolf](https://github.com/falexwolf) | 2023-02-16 | 0.4.2
🚸 Add version integrity checks | [94](https://github.com/laminlabs/laminhub-rest/pull/94) | [falexwolf](https://github.com/falexwolf) | 2023-02-16 |
🎨 Ensure a release was made before deploying a migration | [93](https://github.com/laminlabs/laminhub-rest/pull/93) | [falexwolf](https://github.com/falexwolf) | 2023-02-16 | 0.4.1
🚚 Add column `breaks_lndb` to `versions_cbwk` table | [92](https://github.com/laminlabs/laminhub-rest/pull/92) | [falexwolf](https://github.com/falexwolf) | 2023-02-16 |
:sparkles: Add get_migrations_latest_installed | [91](https://github.com/laminlabs/laminhub-rest/pull/91) | [falexwolf](https://github.com/falexwolf) | 2023-02-16 |
✅ Automatically track migrations | [90](https://github.com/laminlabs/laminhub-rest/pull/90) | [falexwolf](https://github.com/falexwolf) | 2023-02-15 | 0.4.0
🔥 Remove backward compat sbclient modules | [89](https://github.com/laminlabs/laminhub-rest/pull/89) | [falexwolf](https://github.com/falexwolf) | 2023-02-15 |
✅ Test signup and signin | [85](https://github.com/laminlabs/laminhub-rest/pull/85) | [fredericenard](https://github.com/fredericenard) | 2023-02-14 |
🚸 Fix error message for sqlite uniqueness | [88](https://github.com/laminlabs/laminhub-rest/pull/88) | [falexwolf](https://github.com/falexwolf) | 2023-02-14 |
⬆️ Upgrade and rename `lndb_setup` to `lndb` (v0.32.0) | [86](https://github.com/laminlabs/laminhub-rest/pull/86) | [bpenteado](https://github.com/bpenteado) | 2023-02-13 | 0.3.2
✅ Test Supabase functions | [74](https://github.com/laminlabs/laminhub-rest/pull/74) | [fredericenard](https://github.com/fredericenard) | 2023-02-11 | 0.3.1
✅ Use static-testuser1 in tests | [84](https://github.com/laminlabs/laminhub-rest/pull/84) | [fredericenard](https://github.com/fredericenard) | 2023-02-10 |
🎨 Set public column in `init_instance` | [83](https://github.com/laminlabs/laminhub-rest/pull/83) | [falexwolf](https://github.com/falexwolf) | 2023-02-09 |
✅ Add test for instance validation | [82](https://github.com/laminlabs/laminhub-rest/pull/82) | [falexwolf](https://github.com/falexwolf) | 2023-02-09 | 0.3.0
🚸 Validate sqlite uniqueness for given `(storage, name)` | [81](https://github.com/laminlabs/laminhub-rest/pull/81) | [falexwolf](https://github.com/falexwolf) | 2023-02-09 |
🐛 Add error message return in `init_instance` | [79](https://github.com/laminlabs/laminhub-rest/pull/79) | [falexwolf](https://github.com/falexwolf) | 2023-02-09 |
✅ Update test to reflect changes in testuser2 owned instances | [78](https://github.com/laminlabs/laminhub-rest/pull/78) | [fredericenard](https://github.com/fredericenard) | 2023-02-09 |
🗃️ Unique constraint on db field | [75](https://github.com/laminlabs/laminhub-rest/pull/75) | [fredericenard](https://github.com/fredericenard) | 2023-02-08 |
🚚 Update migration file name | [76](https://github.com/laminlabs/laminhub-rest/pull/76) | [fredericenard](https://github.com/fredericenard) | 2023-02-08 |
🚸 Validate storage arg and db arg | [73](https://github.com/laminlabs/laminhub-rest/pull/73) | [falexwolf](https://github.com/falexwolf) | 2023-02-07 |
🍱 Add `hedera` schema module and improve schema validation | [72](https://github.com/laminlabs/laminhub-rest/pull/72) | [falexwolf](https://github.com/falexwolf) | 2023-02-07 |
🚚 Remove `_sbclient` suffix | [71](https://github.com/laminlabs/laminhub-rest/pull/71) | [falexwolf](https://github.com/falexwolf) | 2023-02-06 | 0.2.1
🐛 Delete account_instance entries before deleting an instance | [69](https://github.com/laminlabs/laminhub-rest/pull/69) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
🎨 Replace ORM versions of init, load and add_storage with sbclient | [70](https://github.com/laminlabs/laminhub-rest/pull/70) | [falexwolf](https://github.com/falexwolf) | 2023-02-06 |
🐛 Fix ambiguous relationship | [67](https://github.com/laminlabs/laminhub-rest/pull/67) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
🚑 Revert not nullable public on instance | [66](https://github.com/laminlabs/laminhub-rest/pull/66) | [falexwolf](https://github.com/falexwolf) | 2023-02-06 | 0.2.0
🗃️ Account instance foreign key | [65](https://github.com/laminlabs/laminhub-rest/pull/65) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
✅ Update tests | [64](https://github.com/laminlabs/laminhub-rest/pull/64) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
🗃️ Make public flag and permission field not nullable | [63](https://github.com/laminlabs/laminhub-rest/pull/63) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
✅ Update tests | [62](https://github.com/laminlabs/laminhub-rest/pull/62) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
🗃️ Create account_instance table and add columns to instance table | [61](https://github.com/laminlabs/laminhub-rest/pull/61) | [fredericenard](https://github.com/fredericenard) | 2023-02-06 |
✨ Retrieve account instances using join | [60](https://github.com/laminlabs/laminhub-rest/pull/60) | [fredericenard](https://github.com/fredericenard) | 2023-02-04 |
✨ Account instances endpoint | [59](https://github.com/laminlabs/laminhub-rest/pull/59) | [fredericenard](https://github.com/fredericenard) | 2023-02-04 |
✨ Enable to get account by handle | [58](https://github.com/laminlabs/laminhub-rest/pull/58) | [fredericenard](https://github.com/fredericenard) | 2023-01-31 |
✅ Update test account | [57](https://github.com/laminlabs/laminhub-rest/pull/57) | [fredericenard](https://github.com/fredericenard) | 2023-01-30 |
🗃️ Add image url field | [56](https://github.com/laminlabs/laminhub-rest/pull/56) | [fredericenard](https://github.com/fredericenard) | 2023-01-30 |
⚡ Generate public url for profile picture | [55](https://github.com/laminlabs/laminhub-rest/pull/55) | [fredericenard](https://github.com/fredericenard) | 2023-01-30 |
🥅 Raise exception if delete_ci_instances fails | [54](https://github.com/laminlabs/laminhub-rest/pull/54) | [fredericenard](https://github.com/fredericenard) | 2023-01-30 |
♻️ Separate Account and Profile | [53](https://github.com/laminlabs/laminhub-rest/pull/53) | [fredericenard](https://github.com/fredericenard) | 2023-01-29 |
♻️ Replace user profile by account | [52](https://github.com/laminlabs/laminhub-rest/pull/52) | [fredericenard](https://github.com/fredericenard) | 2023-01-29 |
👷 Clean users created by CI | [51](https://github.com/laminlabs/laminhub-rest/pull/51) | [fredericenard](https://github.com/fredericenard) | 2023-01-27 | 0.1.4
🔥 Drop auxuser table | [50](https://github.com/laminlabs/laminhub-rest/pull/50) | [fredericenard](https://github.com/fredericenard) | 2023-01-24 |
🔥 Drop auxuser table | [49](https://github.com/laminlabs/laminhub-rest/pull/49) | [fredericenard](https://github.com/fredericenard) | 2023-01-24 |
✅ Add auxiliary user table and add back migration tests | [47](https://github.com/laminlabs/laminhub-rest/pull/47) | [falexwolf](https://github.com/falexwolf) | 2023-01-23 |
🐛 Fix exception in `load_instance_sbclient`  | [45](https://github.com/laminlabs/laminhub-rest/pull/45) | [falexwolf](https://github.com/falexwolf) | 2023-01-20 | 0.1.3
✅ Test endpoints | [44](https://github.com/laminlabs/laminhub-rest/pull/44) | [fredericenard](https://github.com/fredericenard) | 2023-01-20 |
💚 Comment out test_model_definitions_match_ddl_postgres | [43](https://github.com/laminlabs/laminhub-rest/pull/43) | [fredericenard](https://github.com/fredericenard) | 2023-01-19 |
💚 Delete ci instances | [41](https://github.com/laminlabs/laminhub-rest/pull/41) | [fredericenard](https://github.com/fredericenard) | 2023-01-18 |
✨ Create delete_instance function | [40](https://github.com/laminlabs/laminhub-rest/pull/40) | [fredericenard](https://github.com/fredericenard) | 2023-01-16 |
✨ Create delete_instance_like function | [39](https://github.com/laminlabs/laminhub-rest/pull/39) | [fredericenard](https://github.com/fredericenard) | 2023-01-16 |
✅ Test get_profile function | [38](https://github.com/laminlabs/laminhub-rest/pull/38) | [fredericenard](https://github.com/fredericenard) | 2023-01-16 |
💄 Prettify sign up & log in logging | [37](https://github.com/laminlabs/laminhub-rest/pull/37) | [falexwolf](https://github.com/falexwolf) | 2023-01-16 |
🐛 Ensure to safely close connection with hub | [34](https://github.com/laminlabs/laminhub-rest/pull/34) | [fredericenard](https://github.com/fredericenard) | 2023-01-16 | 0.1.2
🐛 Fix import error in routers utils due to API change | [33](https://github.com/laminlabs/laminhub-rest/pull/33) | [fredericenard](https://github.com/fredericenard) | 2023-01-16 |
⬆️ Upgrade `lndb-setup` | [32](https://github.com/laminlabs/laminhub-rest/pull/32) | [falexwolf](https://github.com/falexwolf) | 2023-01-16 | 0.1.1
🚚 Move `_hub.py` from `lndb-setup` here, rename to `_sign_upin.py` | [31](https://github.com/laminlabs/laminhub-rest/pull/31) | [falexwolf](https://github.com/falexwolf) | 2023-01-16 | 0.1.0
🐛 Use account table | [30](https://github.com/laminlabs/laminhub-rest/pull/30) | [fredericenard](https://github.com/fredericenard) | 2023-01-15 |
🍱 Autogenerate ER diagram for each migration | [29](https://github.com/laminlabs/laminhub-rest/pull/29) | [falexwolf](https://github.com/falexwolf) | 2023-01-15 |
🏗️ Introduce `init_instance()`, refactor `Organization`, `Storage`, `Instance`, repurpose `Usermeta` to `Account` | [28](https://github.com/laminlabs/laminhub-rest/pull/28) | [falexwolf](https://github.com/falexwolf) | 2023-01-14 | 0.0.2
🚀 Deploy with cloud run | [27](https://github.com/laminlabs/laminhub-rest/pull/27) | [fredericenard](https://github.com/fredericenard) | 2023-01-14 |
🚚 Migrate hub to version 0.0.1 | [26](https://github.com/laminlabs/laminhub-rest/pull/26) | [falexwolf](https://github.com/falexwolf) | 2023-01-13 | 0.0.1
👷 Clean up CI config and add a migrations docs page | [25](https://github.com/laminlabs/laminhub-rest/pull/25) | [falexwolf](https://github.com/falexwolf) | 2023-01-13 |
📝 Clean up docs | [24](https://github.com/laminlabs/laminhub-rest/pull/24) | [falexwolf](https://github.com/falexwolf) | 2023-01-13 |
✅ Clean up tables in hub and start testing migrations | [23](https://github.com/laminlabs/laminhub-rest/pull/23) | [falexwolf](https://github.com/falexwolf) | 2023-01-13 |
🔨 Create deployment pipeline | [20](https://github.com/laminlabs/laminhub-rest/pull/20) | [fredericenard](https://github.com/fredericenard) | 2023-01-13 |
♻️ Simplify `Usermeta` | [22](https://github.com/laminlabs/laminhub-rest/pull/22) | [falexwolf](https://github.com/falexwolf) | 2023-01-13 |
➕ Add lndb-setup dependency | [21](https://github.com/laminlabs/laminhub-rest/pull/21) | [fredericenard](https://github.com/fredericenard) | 2023-01-13 |
♻️ Minimal backend | [19](https://github.com/laminlabs/laminhub-rest/pull/19) | [fredericenard](https://github.com/fredericenard) | 2023-01-13 |
🐛 Handle case where usermeta does not exists | [16](https://github.com/laminlabs/laminhub-rest/pull/16) | [fredericenard](https://github.com/fredericenard) | 2023-01-13 |
⬆️ Upgrade dependencies | [18](https://github.com/laminlabs/laminhub-rest/pull/18) | [fredericenard](https://github.com/fredericenard) | 2023-01-13 |
🔥 Comment out migration tests | [17](https://github.com/laminlabs/laminhub-rest/pull/17) | [fredericenard](https://github.com/fredericenard) | 2023-01-13 |
✅ Test migrations | [14](https://github.com/laminlabs/laminhub-rest/pull/14) | [falexwolf](https://github.com/falexwolf) | 2023-01-05 |
Remove lndb-rest dependency | [15](https://github.com/laminlabs/laminhub-rest/pull/15) | [fredericenard](https://github.com/fredericenard) | 2023-01-05 |
✨ Add migrations infra | [13](https://github.com/laminlabs/laminhub-rest/pull/13) | [falexwolf](https://github.com/falexwolf) | 2023-01-04 |
♻️ Move models into schema submodule | [12](https://github.com/laminlabs/laminhub-rest/pull/12) | [falexwolf](https://github.com/falexwolf) | 2023-01-04 |
✅ Check versions | [10](https://github.com/laminlabs/laminhub-rest/pull/10) | [fredericenard](https://github.com/fredericenard) | 2022-12-05 |
✅ Add unit tests for the two main endpoints | [9](https://github.com/laminlabs/laminhub-rest/pull/9) | [fredericenard](https://github.com/fredericenard) | 2022-12-05 |
Set up test environment | [8](https://github.com/laminlabs/laminhub-rest/pull/8) | [fredericenard](https://github.com/fredericenard) | 2022-12-05 |
Update run script | [6](https://github.com/laminlabs/laminhub-rest/pull/6) | [fredericenard](https://github.com/fredericenard) | 2022-12-01 |
🎨 Rename package | [4](https://github.com/laminlabs/laminhub-rest/pull/4) | [fredericenard](https://github.com/fredericenard) | 2022-11-30 |
Improve initialization scripts | [3](https://github.com/laminlabs/laminhub-rest/pull/3) | [fredericenard](https://github.com/fredericenard) | 2022-11-25 |
Create initialization scripts | [2](https://github.com/laminlabs/laminhub-rest/pull/2) | [fredericenard](https://github.com/fredericenard) | 2022-11-24 |
✨ Implement basic hub endpoints | [1](https://github.com/laminlabs/laminhub-rest/pull/1) | [fredericenard](https://github.com/fredericenard) | 2022-11-18 |
