# Export Gemini Context

ปลั๊กอิน Antigravity สำหรับสร้าง handoff ที่ตรวจสอบย้อนกลับได้จากโค้ดจริง
ไปยัง Gemini เพื่อวางแผนงานสถาปัตยกรรม โดยไม่ให้แผนจากภายนอกกลายเป็นสิทธิ์
แก้ไขโค้ดโดยอัตโนมัติ

โปรเจกต์นี้ทำงานเป็นวงจรที่มีมนุษย์เป็นจุดอนุมัติ:

~~~mermaid
flowchart LR
    A["Workspace snapshot"] --> B["Sanitized GEMINI_CONTEXT.md"]
    B --> C["Gemini planning"]
    C --> D["Draft AGY_CHANGE_REQUEST.md"]
    D --> E["AGY Phase 1 revalidation"]
    E -->|Ready| F["AGY Phase 2 implementation"]
    E -->|Blocked / Drift| G["User guidance"]
    G --> F
~~~

## สิ่งที่ได้

- สรุป workspace แบบ evidence-bound: อ้างอิง path และบรรทัด ไม่เดาพฤติกรรม
- ใช้ budget เริ่มต้นประมาณ 12,000 tokens แบบ progressive/tiered extraction
  แทนการคัดลอกโค้ดทั้ง repository
- ปกป้อง secret, private key, JWT, connection string, cloud identifier,
  Supabase/Firebase credential และข้อมูลส่วนบุคคลด้วย redaction policy
- รู้จัก boundary สมัยใหม่ เช่น Next.js App Router/RSC/Server Actions, Flutter
  state management, Go/Rust module และ Prisma/Drizzle schema
- ทำให้แผนจาก Gemini เป็นเพียง draft แล้วให้ AGY ตรวจ Git state, source hash
  และ public contract ใหม่ก่อนแก้โค้ด
- รันแบบ One-shot ได้อย่างปลอดภัย: Revalidate ตรวจ Git state, source hash และ contract ก่อนเริ่ม implement ทันทีในลูปเดียว

สิ่งที่ปลั๊กอินนี้ **ไม่** ทำโดยค่าเริ่มต้น: รันแอป, ติดตั้ง dependency,
ติดต่อบริการภายนอก, อัปโหลดไฟล์, รัน migration, deploy, หรือเขียนโค้ดระหว่าง
ขั้น export

## ติดตั้ง

ปลั๊กอินใช้โครงสร้างมาตรฐานของ Antigravity: manifest ที่ root และ skills ใต้
โฟลเดอร์ skills. เมื่อ Antigravity โหลด skill แล้ว ชื่อ skill จะเป็น slash
command โดยอัตโนมัติ ตามเอกสาร [Agent Skills](https://antigravity.google/docs/skills)
และ [Plugins](https://www.antigravity.google/docs/plugins?tab=cli)

### ตัวเลือก A: ติดตั้งเป็น plugin ผ่าน AGY CLI

จาก terminal ให้ชี้ไปที่โฟลเดอร์นี้:

~~~bash
agy plugin install "path/to/export-gemini-context"
agy plugin list --json
~~~

คำสั่ง list ควรแสดง plugin ชื่อ export-gemini-context และ skills สองรายการ:
export-gemini-context กับ agy-implementation

### ตัวเลือก B: ใช้เฉพาะ workspace นี้

คัดลอกโฟลเดอร์ plugin ทั้งก้อนไปที่:

~~~text
your-workspace/
  .agents/
    plugins/
      export-gemini-context/
        plugin.json
        skills/
          export-gemini-context/
          agy-implementation/
~~~

หรือถ้าต้องการใช้เป็น workspace skills โดยไม่ติดตั้ง plugin ให้คัดลอกแต่ละ
โฟลเดอร์จาก source-of-truth นี้:

~~~text
skills/export-gemini-context/  ->  your-workspace/.agents/skills/export-gemini-context/
skills/agy-implementation/     ->  your-workspace/.agents/skills/agy-implementation/
~~~

ไม่มีสำเนา skill ซ่อนอยู่ใต้ .agents ภายใน package นี้ เพื่อไม่ให้เกิด content
drift ระหว่าง source สองชุด

## ใช้งานอย่างรวดเร็ว

### 1. Export context

ใน Antigravity ใช้:

~~~text
/export-gemini-context
~~~

ตัวเลือกเป็นคำใบ้ในภาษาธรรมชาติ ไม่จำเป็นต้องเป็น parser syntax เคร่งครัด:

~~~text
/export-gemini-context scope="apps/web" detail=deep budget=12000
/export-gemini-context refresh GEMINI_CONTEXT.md for the auth flow
/export-gemini-context scope=workspace verification=none appendices=none
~~~

หากมี GEMINI_CONTEXT.md อยู่แล้ว ต้องระบุ refresh, replace, overwrite หรือให้
อนุญาตชัดเจนก่อนแทนที่ไฟล์เดิม

ก่อนส่งออก agent จะ:

1. เก็บ snapshot ของ Git/worktree ก่อนเขียน artifact
2. ทำ inventory แบบกรองแล้ว และจัดความสำคัญด้วย T0 ถึง T4
3. สรุป public signatures, routes, schemas และ critical flows ก่อนคัดลอก body
   ของฟังก์ชัน
4. redact ก่อนนำ excerpt เข้าเอกสาร และตรวจ artifact อีกครั้งเมื่อมีเครื่องมือ
   local ที่เชื่อถือได้
5. สร้าง GEMINI_CONTEXT.md เพียงไฟล์เดียว เว้นแต่คุณอนุมัติ appendix เพิ่ม

### 2. วางแผนใน Gemini

1. เปิด Gemini หรือ Gem ที่คุณควบคุมได้
2. วางเนื้อหาจาก prompts/gemini-planning.md เป็น instructions
3. อัปโหลด GEMINI_CONTEXT.md และทุก appendix ที่ถูกอ้างถึง
4. บอก feature, business outcome และ constraints
5. บันทึกผลลัพธ์เป็น AGY_CHANGE_REQUEST.md ที่ root ของ target workspace

Prompt จะกำหนดให้ Gemini แยก FACT, INFERENCE, DOCUMENTED, VERIFIED,
UNKNOWN และ PROPOSAL; เก็บ hash/contract baseline ที่มีอยู่; และตั้ง
implementation_approved เป็น false เสมอ

### 3. Revalidate และ implement ใน Antigravity

ใช้:

~~~text
/agy-implementation
~~~

Phase 1 จะไม่แก้ไฟล์ แต่เปรียบเทียบ:

- branch, commit, tree state และ staged/unstaged/untracked files;
- raw-byte SHA-256 ของ critical files ที่ปลอดภัย;
- public signatures, routes, schemas, authz, migrations และ framework-specific
  boundaries ที่กระทบ;
- project rules, dependencies, verification commands และ user changes ที่ต้อง
  preserve

รายงานจะให้ snapshot_assessment, drift_impact, readiness และ revalidation ID ใหม่:
- **หาก readiness เป็น `READY_FOR_APPROVAL`:** AGY จะดำเนินการเข้าสู่ Phase 2 (Implementation & Verification) ต่อทันทีในเทิร์นเดียวกันโดยอัตโนมัติ ทำให้สั่งครั้งเดียวแล้วได้ผลลัพธ์ครบวงจร
- **หากติดขัด (เช่น `BLOCKED` หรือ `NEEDS_REPLAN`):** AGY จะหยุดรายงาน blocker เพื่อให้คุณพิจารณาก่อนดำเนินงาน

ก่อน Phase 2 AGY จะตรวจ freshness อีกครั้ง หาก Git state หรือ contract ที่
เกี่ยวข้องเปลี่ยนไป จะย้อนกลับไป Phase 1 แทนการเดาต่อ

## วิธีบริหาร Token และ Context

Export ไม่ได้ตัดโค้ดแบบ first-come-first-served แต่ใช้ลำดับดังนี้:

| Tier | เนื้อหา | เหตุผล |
| --- | --- | --- |
| T0 | ทุก module/package ที่พบ | ไม่สูญเสียภาพรวม monorepo |
| T1 | entry point, responsibility, dependency direction | เห็น architecture โดยไม่กิน token |
| T2 | public signatures, routes, schemas, events, migrations | เก็บ compatibility contract |
| T3 | focused critical-flow excerpts | พิสูจน์ behavior ข้าม boundary |
| T4 | หลักฐานเพิ่มเฉพาะคำถามสำคัญ | ใช้เมื่อ planner ต้องตัดสินใจจริง |

ค่าเริ่มต้นแบ่ง budget โดยประมาณเป็น architecture 17%, contracts/data/API
25%, critical flow 23%, operations/rules 12%, snapshot/privacy 8%, และ
risk/coverage/reserve 15%. เมื่อตึง budget จะลด boilerplate ก่อน ไม่ตัด public
contract หรือ unknowns แบบเงียบ ๆ

## Security model และข้อควรตรวจด้วยมนุษย์

| สิ่งที่พบ | พฤติกรรม |
| --- | --- |
| environment/credential/private-key stores | ไม่เปิดเนื้อหาเพื่อหา metadata |
| Docker/CI/Terraform/Kubernetes/example config | อ่านแบบ redact-before-extract หรือ omit |
| JWT, API token, connection string, cookies | redact ทั้งค่า ไม่เก็บ prefix/suffix/hash |
| AWS account/ARN/IAM role, private URL | redact เป็น sensitive infrastructure identifier |
| Supabase/Firebase identifier, anon/service-role key | redact โดย default |
| secret candidate ที่ตรวจไม่ปลอดภัย | omit และบันทึกเฉพาะ category |

Placeholder ที่ควรเห็นใน artifact มีลักษณะเช่น:

- &lt;REDACTED_SECRET:ENV_VAR_NAME&gt;
- &lt;REDACTED_CREDENTIAL:CONNECTION_STRING&gt;
- &lt;REDACTED_PRIVATE_KEY&gt;
- &lt;REDACTED_CLOUD_IDENTIFIER:AWS_IAM&gt;

การ scan เป็น defense in depth ไม่ใช่หลักฐานว่าไม่มี secret เหลืออยู่ จึงต้องเปิด
อ่าน GEMINI_CONTEXT.md ที่สร้างเสร็จก่อนอัปโหลดเสมอ

## การรองรับ Framework

| กลุ่ม | สิ่งที่ export เน้น |
| --- | --- |
| Next.js 14/15 | App Router, RSC/use-client, Server Actions/use-server, route handlers, middleware, cache/revalidate, env boundary |
| Flutter | bootstrap, navigation, state ownership, Provider/Riverpod/BLoC/Redux/signals, repository/platform channel |
| Go | go.work/go.mod, cmd/internal, exported interfaces, handler, context, worker lifecycle |
| Rust | Cargo workspace/features, crate public API, build.rs/proc macro surface, async/error boundary |
| Prisma/Drizzle | schema, migration, relation/index/constraint, transaction, generated-client boundary |
| Microservices | service ownership, API/event contracts, retry/idempotency, queue/worker, redacted deployment topology |

Framework support means evidence-aware discovery. มันไม่อ้างว่า runtime หรือ
deployment ทำงานจนกว่าจะมีการตรวจที่ได้รับอนุญาต

## โครงสร้าง package

~~~text
export-gemini-context/
  plugin.json
  skills/
    export-gemini-context/
      SKILL.md
    agy-implementation/
      SKILL.md
  prompts/
    gemini-planning.md
    agy-implementation.md
  scripts/
    validate_package.py
  .gitignore
  LICENSE
  README.md
~~~

ไฟล์ใต้ skills คือ source-of-truth เดียวของ skill ทั้งสองตัว

## ตรวจ package ก่อนเผยแพร่

ใช้ Python มาตรฐาน ไม่ต้องติดตั้ง package เพิ่ม:

~~~bash
python scripts/validate_package.py
~~~

Validator ตรวจ manifest schema shape, JSON, YAML frontmatter แบบพื้นฐาน,
required artifacts และการไม่มี mirror skill เก่าที่ทำให้เกิด drift ได้
มันเป็น static smoke test ไม่ใช่การรับรองว่า Antigravity runtime โหลด plugin สำเร็จ
บนทุกเวอร์ชัน

ก่อน release:

1. รัน validator
2. ติดตั้งใน workspace ทดสอบด้วย AGY plugin install หรือ placement ที่เอกสารระบุ
3. ตรวจว่า slash commands ปรากฏและอ่าน instructions ถูกต้อง
4. ทดสอบ export fixture ที่มี source injection และ synthetic secrets
5. tag release ใน Git แทนการเพิ่ม field version ที่ไม่อยู่ใน official plugin schema

## License

MIT. ดูไฟล์ LICENSE
