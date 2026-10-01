import logging
from sqlalchemy.orm import Session
from .models import (
    User,
    UserProfile,
    Property,
    Document,
    Sp3kApplication,
    Sp3kStep,
    MortgageAdvisor,
    Notification
)
from .auth import hash_password

logger = logging.getLogger(__name__)


def seed_database(db: Session) -> None:
    try:
        dimas_user = db.query(User).filter(User.email == "dimas@nusaproperty.com").first()
        if not dimas_user:
            dimas_user = User(
                id="usr_dimas",
                email="dimas@nusaproperty.com",
                hashed_password=hash_password("dimas123"),
                full_name="Dimas Nugraha",
                phone="081234567890"
            )
            db.add(dimas_user)
            db.flush()

        dimas_profile = db.query(UserProfile).filter(UserProfile.user_id == dimas_user.id).first()
        if not dimas_profile:
            existing_profile = db.query(UserProfile).first()
            if existing_profile and not existing_profile.user_id:
                existing_profile.user_id = dimas_user.id
            else:
                dimas_profile = UserProfile(
                    id="user_dimas_profile",
                    user_id=dimas_user.id,
                    name="Dimas Nugraha",
                    greeting="Halo",
                    subtitle="Selamat pagi, wujudkan rumah impianmu hari ini.",
                    plafon_estimate=650_000_000,
                    financial_score="Sangat Baik (A+)",
                    financial_score_grade="A+"
                )
                db.add(dimas_profile)

        if db.query(Property).count() == 0:
            sample_properties = [
                Property(
                    id="prop_botanical_a12",
                    title="Cluster Botanical Hills A-12",
                    location="Cikarang Selatan, Bekasi",
                    price=450_000_000,
                    price_formatted="Rp 450.000.000",
                    installment_estimate="Cicilan mulai Rp 2,3 Jt/bln",
                    bedrooms=2,
                    bathrooms=1,
                    carports=1,
                    building_area=36,
                    surface_area=60,
                    electricity_va=1300,
                    certificate_type="SHM",
                    tag_text="Subsidi",
                    tag_type="SUBSIDI",
                    image_url="https://images.unsplash.com/photo-1570129477492-45c003edd2be",
                    developer_name="Harmoni Land Group (Verified Partner)",
                    address_detail="Jl. Raya Serang - Cibarusah, Cikarang Selatan, Bekasi",
                    is_favorite=False,
                    is_featured=True
                ),
                Property(
                    id="prop_grand_harmoni_b4",
                    title="Grand Harmoni City Blok B-04",
                    location="Cibarusah, Bekasi",
                    price=385_000_000,
                    price_formatted="Rp 385.000.000",
                    installment_estimate="Cicilan mulai Rp 1,9 Jt/bln",
                    bedrooms=2,
                    bathrooms=1,
                    carports=1,
                    building_area=30,
                    surface_area=60,
                    electricity_va=1300,
                    certificate_type="SHM",
                    tag_text="Promo DP 0%",
                    tag_type="PROMO",
                    image_url="https://images.unsplash.com/photo-1580587771525-78b9dba3b914",
                    developer_name="Harmoni Land Group",
                    address_detail="Jl. Cibarusah Raya KM 12, Bekasi",
                    is_favorite=False,
                    is_featured=False
                ),
                Property(
                    id="prop_emerald_garden_c9",
                    title="Emerald Garden Residence C-09",
                    location="Serang Baru, Bekasi",
                    price=520_000_000,
                    price_formatted="Rp 520.000.000",
                    installment_estimate="Cicilan mulai Rp 2,7 Jt/bln",
                    bedrooms=3,
                    bathrooms=2,
                    carports=1,
                    building_area=45,
                    surface_area=72,
                    electricity_va=2200,
                    certificate_type="SHM",
                    tag_text="Diskon Biaya Akad",
                    tag_type="DISCOUNT",
                    image_url="https://images.unsplash.com/photo-1512917774080-9991f1c4c750",
                    developer_name="Mitra Graha Sentosa",
                    address_detail="Kawasan Hijau Serang Baru, Bekasi",
                    is_favorite=False,
                    is_featured=False
                )
            ]
            for p in sample_properties:
                db.add(p)

        if db.query(Document).count() == 0:
            sample_docs = [
                Document(
                    id="doc_ktp",
                    title="e-KTP Pemohon & Pasangan",
                    description="Foto e-KTP jelas, tidak terpotong, dan dapat terbaca OCR.",
                    status="VERIFIED",
                    status_label="Terverifikasi",
                    file_name="e-KTP_Dimas_Nugraha.pdf",
                    file_meta="Ukuran berkas 1.8 MB",
                    action_label="Ganti",
                    order_index=1
                ),
                Document(
                    id="doc_npwp",
                    title="NPWP Pribadi",
                    description="Nomor Pokok Wajib Pajak aktif validasi Kemenkeu.",
                    status="VERIFIED",
                    status_label="Terverifikasi",
                    file_name="NPWP_Dimas_Nugraha.pdf",
                    file_meta="Ukuran berkas 950 KB",
                    action_label="Ganti",
                    order_index=2
                ),
                Document(
                    id="doc_slip_gaji",
                    title="Slip Gaji (3 Bulan Terakhir)",
                    description="Slip gaji resmi bertanda tangan HRD atau bermeterai.",
                    status="REQUIRED",
                    status_label="Dibutuhkan",
                    file_name=None,
                    file_meta=None,
                    action_label="Unggah Berkas",
                    order_index=3
                ),
                Document(
                    id="doc_rekening_koran",
                    title="Rekening Koran (3 Bulan Terakhir)",
                    description="Mutasi bank tempat payroll atau rekening usaha aktif.",
                    status="REQUIRED",
                    status_label="Dibutuhkan",
                    file_name=None,
                    file_meta=None,
                    action_label="Unggah Berkas",
                    order_index=4
                )
            ]
            for d in sample_docs:
                db.add(d)

        if db.query(MortgageAdvisor).count() == 0:
            advisor = MortgageAdvisor(
                name="Rian Anggara",
                role="Senior Mortgage Advisor",
                bank="Bank Mandiri Rekanan",
                phone="081234567890",
                is_online=True
            )
            db.add(advisor)
 
        if db.query(Sp3kApplication).count() == 0:
            sp3k = Sp3kApplication(
                registration_number="KPR-2026-NUSA-0918",
                developer="Harmoni Land Group",
                unit_name="Cluster Botanical Hills Blok A-12",
                approved_amount=405_000_000,
                interest_rate_text="4.88% p.a. Fixed 3 Tahun",
                monthly_installment=2_480_000,
                tenor_years=20,
                dp_paid=45_000_000,
                status="APPROVED",
                akad_date="Senin, 6 Oktober 2026 10:00 - 11:30 WIB",
                akad_location="KC Bank Mandiri Cikarang City Walk"
            )
            db.add(sp3k)
            db.flush()

            steps = [
                Sp3kStep(
                    registration_number=sp3k.registration_number,
                    step_number=1,
                    title="Verifikasi Data & Dokumen Akhir",
                    subtitle="Seluruh berkas finansial dan identitas telah tervalidasi oleh analis kredit perbankan.",
                    status="FINISHED",
                    status_badge_text="Selesai"
                ),
                Sp3kStep(
                    registration_number=sp3k.registration_number,
                    step_number=2,
                    title="Pemilihan Jadwal Akad Kredit",
                    subtitle="Pilih tanggal dan lokasi kantor cabang bank atau notaris untuk tanda tangan basah.",
                    status="ACTIVE",
                    status_badge_text="Langkah Selanjutnya"
                ),
                Sp3kStep(
                    registration_number=sp3k.registration_number,
                    step_number=3,
                    title="Pembayaran Biaya Administrasi & Notaris",
                    subtitle="Pelunasan biaya asuransi jiwa, kebakaran, dan legalitas notaris di hari penandatanganan.",
                    status="UPCOMING",
                    status_badge_text="Menunggu Akad"
                )
            ]
            for s in steps:
                db.add(s)

        if db.query(Notification).count() == 0:
            notifications = [
                Notification(
                    title="Pengajuan KPR Disetujui!",
                    message="Selamat! Pengajuan KPR untuk Cluster Botanical Hills A-12 telah disetujui bank rekanan.",
                    type="SUCCESS"
                ),
                Notification(
                    title="Validasi Dokumen Selesai",
                    message="Dokumen e-KTP & NPWP Anda telah tervalidasi 100% oleh sistem verifikasi.",
                    type="INFO"
                ),
                Notification(
                    title="Simulasi Angsuran Terbaru",
                    message="Simak suku bunga promo 4.88% terbaru di fitur Kalkulator KPR Pintar.",
                    type="PROMO"
                )
            ]
            for n in notifications:
                db.add(n)

        db.commit()
    except Exception as e:
        db.rollback()
        logger.warning(f"Seeding database encountered an issue: {e}")
