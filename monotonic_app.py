import random
from typing import Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

from monotonic_cli import (
    MAX_RECURSIVE_LEN,
    check_monotonic_iterative,
    check_monotonic_recursive,
    measure_time,
)

TRIALS = 5
MAX_PLOT_POINTS = 300


def _random_digit_string(length: int, rng: random.Random) -> str:
    return "".join(rng.choices("0123456789", k=length))


def _inject_css() -> None:
    st.markdown(
        """
        <style>
          :root {
            --card: rgba(17, 24, 39, 0.85);
            --border: rgba(148, 163, 184, 0.18);
            --text: rgba(226, 232, 240, 0.92);
            --muted: rgba(226, 232, 240, 0.70);
            --shadow: 0 14px 30px rgba(0,0,0,0.30);
          }

          .stApp {
            background:
              radial-gradient(1200px 800px at 10% 0%, rgba(59, 130, 246, 0.25), transparent 60%),
              radial-gradient(900px 600px at 90% 10%, rgba(16, 185, 129, 0.18), transparent 55%),
              linear-gradient(180deg, rgba(2, 6, 23, 0.95), rgba(11, 18, 32, 0.98));
          }

          div.block-container {
            padding-top: 2.2rem;
            padding-bottom: 4rem;
            max-width: 980px;
          }

          header[data-testid="stHeader"] { background: transparent; }

          .hero {
            padding: 1.25rem 1.35rem;
            border-radius: 22px;
            border: 1px solid var(--border);
            background: linear-gradient(135deg,
              rgba(59, 130, 246, 0.22),
              rgba(99, 102, 241, 0.14),
              rgba(16, 185, 129, 0.10)
            );
            box-shadow: var(--shadow);
          }

          .hero-title {
            font-size: 2.05rem;
            font-weight: 800;
            line-height: 1.1;
            margin: 0;
            color: var(--text);
          }

          .hero-subtitle {
            margin-top: 0.45rem;
            font-size: 1.05rem;
            color: var(--muted);
          }

          .card {
            padding: 1.05rem 1.15rem;
            border-radius: 18px;
            border: 1px solid var(--border);
            background: var(--card);
            box-shadow: var(--shadow);
          }

          .card-title {
            font-size: 1.05rem;
            font-weight: 750;
            margin: 0;
            color: var(--text);
          }

          .card-muted {
            margin-top: 0.35rem;
            color: var(--muted);
            font-size: 0.95rem;
          }

          .badge {
            display: inline-block;
            padding: 0.22rem 0.6rem;
            border-radius: 999px;
            border: 1px solid rgba(255, 255, 255, 0.14);
            font-weight: 650;
            font-size: 0.82rem;
            letter-spacing: 0.2px;
            white-space: nowrap;
          }
          .badge-up { background: rgba(16, 185, 129, 0.20); color: #a7f3d0; }
          .badge-down { background: rgba(249, 115, 22, 0.18); color: #fed7aa; }
          .badge-no { background: rgba(239, 68, 68, 0.18); color: #fecaca; }
          .badge-na { background: rgba(148, 163, 184, 0.18); color: rgba(226, 232, 240, 0.85); }

          .metric {
            font-size: 1.55rem;
            font-weight: 800;
            color: var(--text);
            margin-top: 0.65rem;
          }
          .metric-unit {
            font-size: 0.95rem;
            font-weight: 650;
            color: var(--muted);
            margin-left: 0.25rem;
          }

          div.stButton > button {
            border-radius: 14px;
            padding: 0.55rem 1rem;
            font-weight: 700;
          }

          div[data-baseweb="input"] input { border-radius: 14px; }

          .divider {
            height: 1px;
            background: rgba(148, 163, 184, 0.18);
            margin: 1.2rem 0 1.0rem 0;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _set_matplotlib_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "none",
            "axes.facecolor": "none",
            "axes.edgecolor": "#334155",
            "axes.labelcolor": "#e2e8f0",
            "xtick.color": "#cbd5e1",
            "ytick.color": "#cbd5e1",
            "text.color": "#e2e8f0",
            "grid.color": "#334155",
            "grid.alpha": 0.55,
        }
    )


def _badge_html(result: Optional[str]) -> str:
    if result is None:
        return '<span class="badge badge-na">N/A</span>'

    key = result.lower().strip()
    if "tidak" in key:
        cls = "badge-no"
    elif "turun" in key:
        cls = "badge-down"
    else:
        cls = "badge-up"
    return f'<span class="badge {cls}">{result}</span>'


def _render_algo_card(
    *,
    title: str,
    result: Optional[str],
    time_ms: Optional[float],
    note: Optional[str] = None,
) -> None:
    if time_ms is None:
        metric_html = '<div class="metric">—<span class="metric-unit">ms</span></div>'
    else:
        metric_html = (
            f'<div class="metric">{time_ms:.6f}<span class="metric-unit">ms</span></div>'
        )
    note_html = f'<div class="card-muted">{note}</div>' if note else ""
    st.markdown(
        f"""
        <div class="card">
          <div style="display:flex; align-items:center; justify-content:space-between; gap:0.75rem;">
            <div class="card-title">{title}</div>
            {_badge_html(result)}
          </div>
          {metric_html}
          <div class="card-muted">Rata-rata dari {TRIALS} percobaan</div>
          {note_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="Analisis Efisiensi Algoritma",
    layout="centered",
)
_inject_css()
_set_matplotlib_style()

st.markdown(
    """
    <div class="hero">
      <div class="hero-title">Aplikasi Perbandingan Algoritma</div>
      <div class="hero-subtitle">Iteratif vs Rekursif — Studi kasus: mengecek bilangan monotonik</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.info(
    "Tujuan: membandingkan performa **iteratif** dan **rekursif** untuk mengecek apakah digit-digit membentuk pola "
    "monotonik: **naik**, **turun**, atau **tidak monotonik**.\n\n"
    "- Iteratif: **O(n)** waktu, **O(1)** memori\n"
    "- Rekursif: **O(n)** waktu, namun ada overhead stack dan **O(n)** memori (call stack)"
)

raw_digits = st.text_input("Masukkan bilangan (digit saja):", value="12345")
digits = (raw_digits or "").strip()

if st.button("Jalankan Algoritma"):
    if not digits:
        st.error("Input tidak boleh kosong.")
    elif not digits.isdigit():
        st.error("Input harus berupa digit saja (0-9).")
    else:
        result_it, time_it = measure_time(check_monotonic_iterative, digits, trials=TRIALS)

        result_rec: Optional[str] = None
        time_rec: Optional[float] = None
        rec_note: Optional[str] = None
        if len(digits) > MAX_RECURSIVE_LEN:
            rec_note = (
                f"Input terlalu panjang untuk rekursif (maks {MAX_RECURSIVE_LEN} digit) "
                "untuk menghindari RecursionError."
            )
        else:
            try:
                result_rec, time_rec = measure_time(
                    check_monotonic_recursive, digits, trials=TRIALS
                )
            except (ValueError, RecursionError) as exc:
                rec_note = f"Gagal: {exc}"

        st.subheader("Hasil & Waktu Eksekusi")
        c1, c2 = st.columns(2, gap="large")
        with c1:
            _render_algo_card(
                title="Iteratif",
                result=result_it,
                time_ms=time_it,
                note="O(n) waktu • O(1) memori",
            )
        with c2:
            _render_algo_card(
                title="Rekursif",
                result=result_rec,
                time_ms=time_rec,
                note=rec_note or "O(n) waktu • O(n) memori",
            )

        st.subheader("Grafik Perbandingan Waktu Eksekusi (ms)")
        labels = ["Iteratif", "Rekursif"]
        values = [time_it, (time_rec if time_rec is not None else 0.0)]
        colors = ["#22c55e", "#ef4444"]

        fig_bar, ax_bar = plt.subplots(figsize=(6.2, 3.6))
        ax_bar.bar(labels, values, color=colors)
        ax_bar.set_ylabel("Waktu (ms)")
        ax_bar.set_title(f"Panjang digit = {len(digits)}")
        ax_bar.grid(True, axis="y", linestyle="--", linewidth=0.6)

        y_max = max(values) if max(values) > 0 else 1.0
        for i, v in enumerate(values):
            if i == 1 and time_rec is None:
                ax_bar.text(i, y_max * 0.02, "N/A", ha="center", va="bottom")
            else:
                ax_bar.text(i, v + y_max * 0.02, f"{v:.6f}", ha="center", va="bottom")
        st.pyplot(fig_bar, use_container_width=True)
        if time_rec is None:
            st.caption("Catatan: waktu rekursif tidak tersedia untuk input di atas batas aman.")

        st.subheader("Grafik Hasil: Digit vs Posisi")
        plot_digits = digits
        truncated = False
        if len(plot_digits) > MAX_PLOT_POINTS:
            plot_digits = plot_digits[:MAX_PLOT_POINTS]
            truncated = True

        ys = [int(ch) for ch in plot_digits]
        xs = list(range(1, len(ys) + 1))

        fig_digits, ax_digits = plt.subplots(figsize=(8, 3.2))
        ax_digits.plot(xs, ys, marker="o", linewidth=1.1, color="#60a5fa")
        ax_digits.set_xlabel("Posisi digit")
        ax_digits.set_ylabel("Digit")
        ax_digits.set_ylim(-0.5, 9.5)
        ax_digits.set_yticks(range(0, 10))
        ax_digits.grid(True, linestyle="--", linewidth=0.6)
        st.pyplot(fig_digits, use_container_width=True)

        if truncated:
            st.caption(
                f"Grafik ditampilkan untuk {MAX_PLOT_POINTS} digit pertama dari total {len(digits)} digit."
            )

st.markdown("---")
st.subheader("Grafik Perbandingan Runtime untuk Berbagai Panjang Digit")
if st.checkbox("Tampilkan grafik runtime (panjang digit = 50 hingga 900, step 50)"):
    with st.spinner("Menghitung runtime... (mohon tunggu)"):
        max_n = min(900, MAX_RECURSIVE_LEN)
        lengths = list(range(50, max_n + 1, 50))
        it_times = []
        rec_times = []

        rng = random.Random(42)
        for n in lengths:
            sample = _random_digit_string(n, rng)

            _, t_it = measure_time(check_monotonic_iterative, sample, trials=TRIALS)
            it_times.append(max(t_it, 1e-6))

            _, t_rec = measure_time(check_monotonic_recursive, sample, trials=TRIALS)
            rec_times.append(max(t_rec, 1e-6))

        fig_rt, ax_rt = plt.subplots(figsize=(8, 4))
        ax_rt.plot(lengths, it_times, "o-", label="Iteratif", color="#22c55e")
        ax_rt.plot(lengths, rec_times, "x--", label="Rekursif", color="#ef4444")
        ax_rt.set_xlabel("Panjang digit (n)")
        ax_rt.set_ylabel("Waktu (ms)")
        ax_rt.set_yscale("log")
        ax_rt.set_title("Runtime vs Panjang Digit (Skala Logaritmik)")
        ax_rt.legend()
        ax_rt.grid(True, which="both", linestyle="--", linewidth=0.6)
        st.pyplot(fig_rt, use_container_width=True)
        st.caption("Input dibuat acak untuk setiap panjang digit. Skala logaritmik digunakan.")
