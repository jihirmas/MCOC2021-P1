from secciones1 import SeccionICHA

# sec1 = SeccionICHA("[]350x150x23.0",base_datos="Perfiles ICHA 1.xlsx")
# print(sec1)

# sec1 = SeccionICHA("[]350x150x23",base_datos="Perfiles ICHA 1.xlsx")
# print(sec1)

# sec2 = SeccionICHA("H1100x350x400.4",base_datos="Perfiles ICHA 1.xlsx")
# print(sec2)

# sec3 = SeccionICHA("[]350x150x23",base_datos="Perfiles ICHA 1.xlsx")
# print(sec3)

l = ['[]400×200×45.6', '[]400×200×36.7', '[]400×200×27.7', '[]400×200×18.6', '[]400×150×41.7', '[]400×150×33.6', '[]400×150×25.4', '[]400×150×17.0', '[]400×100×37.8', '[]400×100×30.5', '[]400×100×23.0', '[]400×100×15.5', '[]350×200×41.7', '[]350×200×33.6', '[]350×200×25.4', '[]350×200×17.0', '[]350×150×37.8', '[]350×150×30.5', '[]350×150×23.0', '[]350×150×15.5', '[]350×100×33.9', '[]350×100×27.3', '[]350×100×20.7', '[]350×100×13.9', '[]300×200×37.8', '[]300×200×30.5', '[]300×200×23.0', '[]300×200×15.5', '[]300×150×33.9', '[]300×150×27.3', '[]300×150×20.7', '[]300×150×13.9', '[]300×100×29.9', '[]300×100×24.2', '[]300×100×18.3', '[]300×100×12.3', '[]300×75×28.0', '[]300×75×22.6', '[]300×75×17.1', '[]300×75×11.5', '[]300×50×26.0', '[]300×50×21.0', '[]300×50×16.0', '[]300×50×10.8', '[]250×200×33.9', '[]250×200×27.3', '[]250×200×20.7', '[]250×200×13.9', '[]250×150×29.9', '[]250×150×24.2', '[]250×150×18.3', '[]250×150×12.3', '[]250×100×26.0', '[]250×100×21.0', '[]250×100×16.0', '[]250×100×10.8', '[]250×75×24.1', '[]250×75×19.5', '[]250×75×14.8', '[]250×75×10.0', '[]250×50×22.1', '[]250×50×17.9', '[]250×50×13.6', '[]250×50×9.2', '[]200×200×29.9', '[]200×200×24.2', '[]200×200×18.3', '[]200×200×12.3', '[]200×150×26.0', '[]200×150×21.0', '[]200×150×16.0', '[]200×150×10.8', '[]200×100×22.1', '[]200×100×17.9', '[]200×100×13.6', '[]200×100×9.2', '[]200×75×20.1', '[]200×75×16.3', '[]200×75×12.4', '[]200×75×8.4', '[]200×70×23.3', '[]200×70×19.7', '[]200×70×16.0', '[]200×50×18.2', '[]200×50×14.8', '[]200×50×11.2', '[]200×50×7.6', '[]150×150×22.1', '[]150×150×17.9', '[]150×150×13.6', '[]150×150×9.2', '[]150×100×18.2', '[]150×100×14.8', '[]150×100×11.2', '[]150×100×7.6', '[]150×75×16.2', '[]150×75×13.2', '[]150×75×10.1', '[]150×75×6.8', '[]150×50×16.7', '[]150×50×14.2', '[]150×50×11.6', '[]150×50×8.9', '[]150×50×6.0', '[]135×135×23.3', '[]135×135×19.7', '[]135×135×16.0', '[]120×60×14.9', '[]120×60×12.7', '[]120×60×10.4', '[]120×60×8.0', '[]100×100×16.7', '[]100×100×14.2', '[]100×100×11.6', '[]100×100×8.9', '[]100×100×6.0', '[]100×75×12.3', '[]100×75×10.1', '[]100×75×7.7', '[]100×75×5.3', '[]100×50×12.0', '[]100×50×10.3', '[]100×50×8.5', '[]100×50×6.5', '[]100×50×4.5', '[]80×40×8.0', '[]80×40×6.6', '[]80×40×5.1', '[]80×40×3.5', '[]75×75×12.0', '[]75×75×10.3', '[]75×75×8.5', '[]75×75×6.5', '[]75×75×4.5', '[]70×30×5.3', '[]70×30×4.2', '[]70×30×2.9', '[]60×40×6.4', '[]60×40×5.3', '[]60×40×4.2', '[]60×40×2.9', '[]60×40×2.2', '[]50×50×7.3', '[]50×50×6.4', '[]50×50×5.3', '[]50×50×4.2', '[]50×50×2.9', '[]50×50×2.2', '[]50×30×3.2', '[]50×30×2.3', '[]50×30×1.8', '[]50×30×1.2', '[]50×20×2.0', '[]50×20×1.5', '[]50×20×1.0', '[]40×40×4.8', '[]40×40×4.1', '[]40×40×3.2', '[]40×40×2.3', '[]40×40×1.8', '[]40×40×1.2', '[]40×30×2.0', '[]40×30×1.5', '[]40×30×1.0', '[]40×20×1.7', '[]40×20×1.3', '[]40×20×0.9', '[]30×30×1.7', '[]30×30×1.3', '[]30×30×0.9', '[]30×20×1.3', '[]30×20×1.0', '[]30×20×0.7', '[]25×25×1.3', '[]25×25×1.0', '[]25×25×0.7', '[]25×15×1.0', '[]25×15×0.8', '[]25×15×0.6', '[]20×20×1.0', '[]20×20×0.8', '[]20×20×0.6', '[]20×10×0.6', '[]20×10×0.4', '[]15×15×0.6', '[]15×15×0.4', '[]12×12×0.3']

for i in  l:
    sec3 = SeccionICHA(i,base_datos="Perfiles ICHA 1.xlsx")
    print(sec3)