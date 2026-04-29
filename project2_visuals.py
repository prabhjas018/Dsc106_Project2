import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('environment.csv')

co2_col = 'average_value_Adjusted savings: carbon dioxide damage (current US$)'
key_countries = ['United States', 'China', 'India', 'Russian Federation',
                 'Germany', 'Japan', 'Brazil', 'Canada']
agg_keywords = ['World', 'income', 'region', 'OECD', 'Euro', 'Arab', 'Asia',
                'Africa', 'Latin', 'Middle', 'South', 'North', 'East', 'Pacific',
                'Caribbean', 'Saharan', 'small', 'island', 'members', 'IDA',
                'IBRD', 'HIPC', 'fragile', 'least', 'Sub', 'demographic']

ts = df[df['Country Name'].isin(key_countries)][['Country Name', 'Year', co2_col]]
cumulative = ts.dropna(subset=[co2_col]).groupby('Country Name')[co2_col].sum() / 1e12
sorted_cum = cumulative.sort_values()

us_ts = ts[ts['Country Name'] == 'United States'].sort_values('Year').dropna(subset=[co2_col])
cn_ts = ts[ts['Country Name'] == 'China'].sort_values('Year').dropna(subset=[co2_col])
in_ts = ts[ts['Country Name'] == 'India'].sort_values('Year').dropna(subset=[co2_col])
ru_ts = ts[ts['Country Name'] == 'Russian Federation'].sort_values('Year').dropna(subset=[co2_col])

# Figure 1: Cumulative CO2 damage by country (FOR)
fig, ax = plt.subplots(figsize=(9, 5))
bar_colors = ['#c0392b' if c == 'United States' else '#aab7b8' for c in sorted_cum.index]
ax.barh(sorted_cum.index, sorted_cum.values, color=bar_colors)
ax.set_xlabel('Cumulative CO2 Damage (Trillions USD)', fontsize=11)
ax.set_title('U.S. Cumulative CO2 Damage Ranks Second Globally (1970-2019)',
             fontsize=12, fontweight='bold', color='#c0392b')
us_val = cumulative['United States']
us_idx = list(sorted_cum.index).index('United States')
ax.annotate(f'USA: ${us_val:.1f}T\n(2nd only to China,\nbut surpassed it\nbefore 2005)',
            xy=(us_val, us_idx), xytext=(us_val + 0.2, 1.0),
            arrowprops=dict(arrowstyle='->', color='#c0392b'),
            color='#c0392b', fontsize=9, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(0, sorted_cum.max() * 1.4)
plt.tight_layout()
plt.savefig('viz_for_1.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 2: Annual CO2 damage trend over time (FOR)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(us_ts['Year'], us_ts[co2_col] / 1e9, color='#c0392b', linewidth=3, label='United States')
ax.plot(cn_ts['Year'], cn_ts[co2_col] / 1e9, color='#aab7b8', linewidth=2, label='China')
ax.plot(in_ts['Year'], in_ts[co2_col] / 1e9, color='#aab7b8', linewidth=1.5, linestyle='--', label='India')
ax.plot(ru_ts['Year'], ru_ts[co2_col] / 1e9, color='#aab7b8', linewidth=1.5, linestyle=':', label='Russia')
ax.axvspan(1970, 2005, alpha=0.07, color='#c0392b')
ax.text(1976, 220, 'US was #1\nfor ~35 years', color='#c0392b', fontsize=9, alpha=0.8)
ax.set_xlabel('Year (1970-2019)', fontsize=11)
ax.set_ylabel('Annual CO2 Damage (Billion USD)', fontsize=11)
ax.set_title('The U.S. Led Annual CO2 Damage for Over Three Decades\nBefore Being Surpassed by China Around 2005',
             fontsize=12, fontweight='bold', color='#c0392b')
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('viz_for_2.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 3: Most recent year (2019) CO2 damage by country (AGAINST)
recent = df[df['Year'] == 2019][['Country Name', co2_col]].dropna()
mask = ~recent['Country Name'].apply(
    lambda x: any(k.lower() in x.lower() for k in agg_keywords))
recent = recent[mask].sort_values(co2_col, ascending=False).head(10)
recent_labels = (recent['Country Name']
                 .str.replace('Russian Federation', 'Russia')
                 .str.replace('Iran, Islamic Rep.', 'Iran')
                 .str.replace('Korea, Rep.', 'S. Korea'))

fig, ax = plt.subplots(figsize=(9, 5))
bar_colors2 = ['#e67e22' if 'China' in c else '#aab7b8' for c in recent['Country Name']]
ax.bar(recent_labels, recent[co2_col] / 1e9, color=bar_colors2)
ax.set_ylabel('Annual CO2 Damage (Billion USD)', fontsize=11)
ax.set_title('China Accounts for the Largest Share of Annual CO2 Damage (2019)',
             fontsize=12, fontweight='bold', color='#e67e22')
ax.tick_params(axis='x', rotation=25, labelsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
cn_val = recent[recent['Country Name'] == 'China'][co2_col].values[0] / 1e9
ax.annotate(f'China: ${cn_val:.0f}B\n(approx. 2.2x USA)',
            xy=(0, cn_val), xytext=(1.2, cn_val - 80),
            arrowprops=dict(arrowstyle='->', color='#e67e22'),
            color='#e67e22', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('viz_against_1.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 4: Indexed growth since 1990, US vs China (AGAINST)
us_norm = us_ts[us_ts['Year'] >= 1990].copy()
cn_norm = cn_ts[cn_ts['Year'] >= 1990].copy()
us_base = us_norm[us_norm['Year'] == 1990][co2_col].values[0]
cn_base = cn_norm[cn_norm['Year'] == 1990][co2_col].values[0]
us_norm['idx'] = us_norm[co2_col] / us_base * 100
cn_norm['idx'] = cn_norm[co2_col] / cn_base * 100

fig, ax = plt.subplots(figsize=(9, 5))
ax.fill_between(cn_norm['Year'], cn_norm['idx'], us_norm['idx'],
                where=cn_norm['idx'].values > us_norm['idx'].values,
                alpha=0.15, color='#e67e22')
ax.plot(cn_norm['Year'], cn_norm['idx'], color='#e67e22', linewidth=3,
        marker='o', markersize=3, label='China')
ax.plot(us_norm['Year'], us_norm['idx'], color='#2980b9', linewidth=3,
        marker='s', markersize=3, label='United States')
ax.axhline(100, color='gray', linestyle=':', alpha=0.5)
ax.set_xlabel('Year (1990-2019)', fontsize=11)
ax.set_ylabel('CO2 Damage Index (1990 = 100)', fontsize=11)
ax.set_title("China's CO2 Damage Has Grown Roughly 5x Since 1990,\nWhile U.S. Levels Have Remained Relatively Stable",
             fontsize=12, fontweight='bold', color='#e67e22')
ax.set_ylim(50, 560)
ax.legend(fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('viz_against_2.png', dpi=150, bbox_inches='tight')
plt.close()

print("All 4 visualizations saved.")