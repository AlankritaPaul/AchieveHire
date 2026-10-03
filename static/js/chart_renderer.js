/**
 * AchieveHire - Interactive SVG Chart & Competency Visualizer
 * Renders radar competency charts, progression bars, and score rings directly in the client.
 */
class CompetencyChartRenderer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    /**
     * Renders a multi-axis Radar Chart for Competency Evaluations
     * @param {Array<{label: string, score: number, maxScore: number}>} competencies
     */
    renderRadarChart(competencies, options = {}) {
        if (!this.container) return;
        const width = options.width || 420;
        const height = options.height || 420;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = (Math.min(width, height) / 2) - 50;
        const totalAxes = competencies.length;
        const angleStep = (Math.PI * 2) / totalAxes;

        // Background grid rings (20%, 40%, 60%, 80%, 100%)
        let gridRingsSvg = '';
        for (let level = 1; level <= 5; level++) {
            const levelRadius = (radius / 5) * level;
            let points = [];
            for (let i = 0; i < totalAxes; i++) {
                const angle = i * angleStep - Math.PI / 2;
                const x = centerX + levelRadius * Math.cos(angle);
                const y = centerY + levelRadius * Math.sin(angle);
                points.push(`${x},${y}`);
            }
            gridRingsSvg += `<polygon points="${points.join(' ')}" fill="none" stroke="#E2E8F0" stroke-width="1.2" stroke-dasharray="2,2"/>`;
        }

        // Axes lines and labels
        let axesSvg = '';
        let labelsSvg = '';
        let polygonPoints = [];

        competencies.forEach((item, index) => {
            const angle = index * angleStep - Math.PI / 2;
            const axisX = centerX + radius * Math.cos(angle);
            const axisY = centerY + radius * Math.sin(angle);
            axesSvg += `<line x1="${centerX}" y1="${centerY}" x2="${axisX}" y2="${axisY}" stroke="#CBD5E1" stroke-width="1.5" />`;

            // Data point
            const ratio = Math.min(1.0, Math.max(0.0, item.score / (item.maxScore || 100)));
            const dataX = centerX + (radius * ratio) * Math.cos(angle);
            const dataY = centerY + (radius * ratio) * Math.sin(angle);
            polygonPoints.push(`${dataX},${dataY}`);

            // Text Label position
            const labelX = centerX + (radius + 25) * Math.cos(angle);
            const labelY = centerY + (radius + 20) * Math.sin(angle);
            const anchor = Math.abs(Math.cos(angle)) < 0.2 ? 'middle' : Math.cos(angle) > 0 ? 'start' : 'end';

            labelsSvg += `
                <text x="${labelX}" y="${labelY}" text-anchor="${anchor}" class="radar-label" fill="#1E293B" font-size="12px" font-weight="600">
                    ${item.label} (${Math.round(item.score)}%)
                </text>
            `;
        });

        const svgContent = `
            <svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" class="achievehire-radar-svg">
                <g class="grid-rings">${gridRingsSvg}</g>
                <g class="axes">${axesSvg}</g>
                <polygon points="${polygonPoints.join(' ')}" fill="rgba(59, 130, 246, 0.35)" stroke="#2563EB" stroke-width="2.5" />
                ${polygonPoints.map(pt => {
                    const [px, py] = pt.split(',');
                    return `<circle cx="${px}" cy="${py}" r="4.5" fill="#1D4ED8" stroke="#FFFFFF" stroke-width="2" />`;
                }).join('')}
                <g class="labels">${labelsSvg}</g>
            </svg>
        `;

        this.container.innerHTML = svgContent;
    }

    /**
     * Renders a Progression Bar Chart for sequential interview rounds
     * @param {Array<{roundName: string, score: number, benchmark: number}>} rounds
     */
    renderProgressionChart(rounds, options = {}) {
        if (!this.container) return;
        const width = options.width || 500;
        const height = options.height || 260;
        const padding = 45;
        const barWidth = 36;
        const chartHeight = height - padding * 2;
        const spacing = (width - padding * 2) / rounds.length;

        let barsSvg = '';
        rounds.forEach((round, index) => {
            const x = padding + index * spacing + (spacing - barWidth) / 2;
            const barHeight = (round.score / 100) * chartHeight;
            const y = height - padding - barHeight;

            let barColor = '#3B82F6';
            if (round.score >= 80) barColor = '#10B981';
            else if (round.score < 60) barColor = '#F59E0B';

            barsSvg += `
                <g class="bar-group">
                    <rect x="${x}" y="${y}" width="${barWidth}" height="${barHeight}" rx="4" fill="${barColor}" class="transition-bar" />
                    <text x="${x + barWidth / 2}" y="${y - 8}" text-anchor="middle" font-size="11px" font-weight="700" fill="#0F172A">
                        ${round.score}%
                    </text>
                    <text x="${x + barWidth / 2}" y="${height - padding + 18}" text-anchor="middle" font-size="11px" font-weight="500" fill="#64748B">
                        ${round.roundName}
                    </text>
                </g>
            `;
        });

        this.container.innerHTML = `
            <svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" class="achievehire-progression-svg">
                <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="#E2E8F0" stroke-width="2" />
                ${barsSvg}
            </svg>
        `;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CompetencyChartRenderer };
} else {
    window.CompetencyChartRenderer = CompetencyChartRenderer;
}
