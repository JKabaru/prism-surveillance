import pandas as pd
import base64
from datetime import datetime

class PRISMReporter:
    def __init__(self):
        pass

    def generate_html_report(self, ring_id, evidence, attribution, graph_bytes=None):
        """
        Generates a standalone, professional HTML evidence brief.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format Indicators
        indicators_html = "".join([f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 12px; margin-bottom: 8px; font-size: 0.9rem; color: #94a3b8;">
                <span style="color: #8b5cf6; margin-right: 8px;">●</span> {ind}
            </div>
        """ for ind in evidence['indicators']])
        
        # Attribution Data
        top_partner = next(iter(attribution['top_partners'])) if attribution['top_partners'] else "Unknown"
        top_sub = next(iter(attribution['top_subs'])) if attribution['top_subs'] else "Unknown"
        
        graph_img = ""
        if graph_bytes:
            b64_graph = base64.b64encode(graph_bytes).decode('utf-8')
            graph_img = f'<img src="data:image/png;base64,{b64_graph}" style="width: 100%; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">'
        else:
            graph_img = """
            <div style="height: 200px; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px;">
                <p style="color: #64748b; font-size: 0.8rem;">Temporal Graph Data Placeholder</p>
            </div>
            """
            
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PRISM Evidence Brief - {ring_id}</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                body {{ 
                    font-family: 'Inter', sans-serif; 
                    background-color: #050505; 
                    background-image: radial-gradient(circle at 10% 10%, rgba(139, 92, 246, 0.05), transparent);
                    color: #e2e8f0; 
                    margin: 0;
                    padding: 40px;
                }}
                .glass-card {{ 
                    background: rgba(13, 13, 13, 0.7); 
                    backdrop-filter: blur(25px); 
                    border: 1px solid rgba(255,255,255,0.08); 
                    border-radius: 20px; 
                    padding: 32px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
                }}
                .neon-magenta {{ text-shadow: 0 0 10px rgba(255, 0, 255, 0.4); color: #ff00ff; }}
                .neon-cyan {{ text-shadow: 0 0 10px rgba(0, 242, 255, 0.4); color: #00f2ff; }}
            </style>
        </head>
        <body class="p-8 md:p-16">
            <div class="max-w-4xl mx-auto">
                <!-- Header -->
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 border-b border-white/5 pb-8 gap-4">
                    <div>
                        <div class="flex items-center gap-3 mb-2">
                             <div class="w-8 h-8 rounded bg-gradient-to-br from-[#00f2ff] via-[#8b5cf6] to-[#ff00ff] flex items-center justify-center">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                             </div>
                             <h1 class="text-2xl font-bold tracking-tight">PRISM <span class="text-slate-500 font-medium">Forensic Brief</span></h1>
                        </div>
                        <p class="text-slate-500 text-sm">Predictive Risk & Instability Surveillance Module</p>
                    </div>
                    <div class="text-left md:text-right">
                        <div class="text-xs font-mono text-slate-500 uppercase tracking-widest mb-1">Generated On</div>
                        <div class="text-sm font-medium">{timestamp}</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div class="glass-card p-6 border-l-4 border-[#ff00ff]">
                        <div class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Case ID</div>
                        <div class="text-xl font-bold font-mono">{ring_id}</div>
                    </div>
                    <div class="glass-card p-6 border-l-4 border-[#8b5cf6]">
                        <div class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Confidence Score</div>
                        <div class="text-xl font-bold neon-magenta">{evidence['confidence']*100:.1f}%</div>
                    </div>
                    <div class="glass-card p-6 border-l-4 border-[#00f2ff]">
                        <div class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Exposure Estimate</div>
                        <div class="text-xl font-bold">${evidence['exposure']:,}</div>
                    </div>
                </div>

                <!-- Hypothesis -->
                <div class="glass-card p-8 mb-8">
                    <h2 class="text-sm font-bold text-slate-500 uppercase tracking-widest mb-4">Fraud Hypothesis</h2>
                    <p class="text-lg leading-relaxed text-slate-300 italic">"{evidence['hypothesis']}"</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
                    <!-- Key Indicators -->
                    <div>
                        <h2 class="text-sm font-bold text-slate-500 uppercase tracking-widest mb-4">Risk Indicators</h2>
                        {indicators_html}
                    </div>

                    <!-- Attribution -->
                    <div>
                        <h2 class="text-sm font-bold text-slate-500 uppercase tracking-widest mb-4">Network Attribution</h2>
                        <div class="glass-card p-6 space-y-4">
                            <div>
                                <div class="text-[10px] font-bold text-slate-600 uppercase tracking-widest mb-1">Primary Partner</div>
                                <div class="text-sm font-semibold">{top_partner}</div>
                            </div>
                            <div class="pt-4 border-t border-white/5">
                                <div class="text-[10px] font-bold text-slate-600 uppercase tracking-widest mb-1">Lead Sub-Affiliate</div>
                                <div class="text-sm font-semibold">{top_sub}</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Network Graph Image -->
                <div class="mb-12">
                    <h2 class="text-sm font-bold text-slate-500 uppercase tracking-widest mb-4 text-center">Temporal Interaction Graph</h2>
                    {graph_img}
                </div>

                <!-- Footer -->
                <div class="text-center border-t border-white/5 pt-8 mt-16">
                    <p class="text-xs text-slate-600 uppercase tracking-widest mb-2">Confidential - Intelligence Brief</p>
                    <p class="text-[10px] text-slate-700">This document contains sensitive agentic analysis and temporal correlation data. Unauthorized distribution is prohibited.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
