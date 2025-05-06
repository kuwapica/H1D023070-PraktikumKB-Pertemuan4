% Sistem Pakar Deteksi Dini Autisme pada Anak

% Fakta-fakta Gejala (G)
gejala(g1, 'Anak tidak melihat ke arah sesuatu yang orang tua atau orang lain tunjuk').
gejala(g2, 'Orang tua pernah berpikir bahwa anaknya tuli').
gejala(g3, 'Anak tidak pernah bermain pura-pura (misalnya pura-pura berbicara menggunakan telepon atau menyuapi boneka)').
gejala(g4, 'Anak tidak pernah menaiki benda-benda (misalnya furniture, alat-alat bermain atau tangga)').
gejala(g5, 'Anak suka menggerakkan jari-jari tangannya dengan cara yang aneh di dekat matanya').
gejala(g6, 'Anak tidak pernah menunjuk dengan satu jari untuk meminta sesuatu atau meminta tolong (menunjuk makanan atau mainan yang jauh dari jangkauannya)').
gejala(g7, 'Anak tidak pernah menunjuk dengan satu jari untuk menunjukkan sesuatu yang menarik kepada orang tua').
gejala(g8, 'Anak tidak tertarik pada anak lainnya (anak anda tidak memperhatikan anak lainnya, tersenyum pada anak lainnya atau pergi ke arah mereka)').
gejala(g9, 'Anak tidak pernah memperlihatkan suatu benda dengan membawanya atau mengangkatnya untuk orang tua').
gejala(g10, 'Anak tidak memberikan respon ketika namanya dipanggil').
gejala(g11, 'Anak tidak tersenyum balik ketika orang tua atau orang lain tersenyum kepadanya').
gejala(g12, 'Anak menjadi marah atau terganggu ketika mendengar suara bising').
gejala(g13, 'Anak tidak bisa berjalan').
gejala(g14, 'Anak tidak menatap mata saat orang tua atau orang lain berbicara kepadanya').
gejala(g15, 'Anak tidak mencoba meniru apa yang dilakukan orang tua atau orang lain').
gejala(g16, 'Anak tidak melihat sekeliling untuk melihat apa yang sedang dilihat ketika orang tua melihat sesuatu').
gejala(g17, 'Anak tidak mencoba untuk membuat orang tua melihat kepadanya (misalnya berkata "lihat" atau "lihat aku")').
gejala(g18, 'Anak tidak mengerti saat orang tua memintanya melakukan sesuatu (anak tidak mengerti kalimat "letakkan itu di meja" atau "ambilkan saya bantal")').
gejala(g19, 'Anak tidak menatap wajah orang tua atau orang lain ketika sesuatau yang baru terjadi untuk melihat perasaan atau tanggapan orang tua atau orang lain tentang hal itu.  (Misalnya, jika anak anda mendengar bunyi aneh atau lucu, atau melihat mainan baru, dia tidak menatap wajah anda)').
gejala(g20, 'Anak tidak menyukai aktivitas yang bergerak (misalnya diayun-ayun atau dihentak-hentakkan pada lutut)').

% Klasifikasi Resiko
resiko(rendah, 'Resiko Rendah', 'Tidak ada tindak lanjutan yang diperlukan, selain pengamatan untuk mengidentifikasi autisme. Jika anak di bawah 24 bulan, maka pemeriksaan dapat diulang lagi pada usia yang lebih tua, untuk mendapatkan data yang stabil.').
resiko(medium, 'Resiko Medium', 'Perlu dilakukan wawancara tindak lanjut dengan psikolog.').
resiko(tinggi, 'Resiko Tinggi', 'Anak beresiko tinggi mengalami gangguan autisme atau hambatan perkembangan lainnya. Anak  harus  segera dirujuk  ke  klinik  tumbuh  kembang  anak, psikolog anak atau dokter spesialis anak.').

% Basis Data Dinamis (untuk menyimpan gejala yang diinput pengguna)
:- dynamic memiliki_gejala/1.
:- dynamic usia_anak/1.
:- dynamic nama_anak/1.
:- dynamic total_skor/1.

% Hapus semua data dinamis
reset_all :-
    retractall(memiliki_gejala(_)),
    retractall(usia_anak(_)),
    retractall(nama_anak(_)),
    retractall(total_skor(_)),
    asserta(total_skor(0)).

% Memulai diagnosis
start :-
    reset_all,
    write('Sistem Pakar diagnosis Dini Autisme pada Anak'), nl,
    write('=============================================='), nl, nl,
    
    write('Masukkan data anak:'), nl,
    write('Nama anak: '),
    read(Nama),
    asserta(nama_anak(Nama)),
    
    write('Usia anak (dalam bulan): '),
    read(Usia),
    asserta(usia_anak(Usia)),
    
    (Usia < 24 ->
        write('Anak berusia di bawah 24 bulan, diagnosis mungkin perlu diulang pada usia yang lebih tua.'), nl
    ; Usia >= 24, Usia =< 36 ->
        write('Anak berusia antara 24-36 bulan, ideal untuk deteksi dini autisme.'), nl
    ;
        write('Anak berusia di atas 36 bulan.'), nl
    ),
    nl,
    
    write('Jawablah pertanyaan berikut dengan y/n:'), nl,
    nl,
    tanya_gejala,
    evaluasi_hasil,
    !.

% Menanyakan semua gejala
tanya_gejala :-
    forall(gejala(Id, Deskripsi),
        (write(Deskripsi), write(' (y/n)? '),
        read(Jawaban),
        (Jawaban = y -> 
            asserta(memiliki_gejala(Id)),
            tambah_skor(1)
        ;
            true
        ),
        nl
        )
    ).

% Menambah skor total
tambah_skor(Nilai) :-
    total_skor(Skor),
    NilaiTotal is Skor + Nilai,
    retract(total_skor(_)),
    asserta(total_skor(NilaiTotal)).

% Evaluasi hasil berdasarkan total skor
evaluasi_hasil :-
    nama_anak(Nama),
    usia_anak(Usia),
    total_skor(Skor),
    
    write('Hasil diagnosis untuk '), write(Nama), write(' ('), write(Usia), write(' bulan):'), nl,
    write('--------------------------------------------------'), nl,
    
    % Tentukan tingkat resiko
    (Skor =< 2 ->
        TingkatResiko = rendah
    ; Skor =< 7 ->
        TingkatResiko = medium
    ;
        TingkatResiko = tinggi
    ),
    
    % Tampilkan hasil resiko dan solusi
    resiko(TingkatResiko, Nama_Resiko, Solusi), % diambil dari data yang di atas
    write('diagnosis: '), write(Nama_Resiko), nl,
    write('Solusi: '), nl,
    write(Solusi), nl,
    nl,
    
    % Tampilkan gejala yang terdeteksi
    write('Gejala yang terdeteksi:'), nl,
    forall(memiliki_gejala(Id),
        (gejala(Id, Deskripsi),
        write('- '), write(Deskripsi), nl)
    ),
    
    write('--------------------------------------------------'), nl,
    write('Catatan: diagnosis ini hanya sebagai rujukan awal.'), nl,
    write('Silakan konsultasikan dengan dokter spesialis anak atau psikolog untuk diagnosis yang lebih akurat.').

% Mulai aplikasi
:- write('Untuk memulai diagnosis, ketik "start." dan tekan Enter.'), nl.