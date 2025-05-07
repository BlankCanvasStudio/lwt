#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random, string


def write_text(text, time_mod=0.2):
    for c in text:
        sec = random.gauss(time_mod, time_mod / 2)
        webdriver.ActionChains(firefox)\
                .send_keys(c)\
                .perform()
        time.sleep(abs(sec))


options = webdriver.FirefoxOptions()
options.add_argument("-headless")
options.add_argument("window-size=1400,600")

firefox = webdriver.Firefox(options=options)

firefox.set_window_size(1920, 1080)

try:
    firefox.get("https://translate.google.com/")
except:
    pass

firefox.implicitly_wait(4)
time.sleep(5)


lorem_sentences = """
Il est important de prendre soin du patient, d'être suivi par le client, mais en même temps il sera affecté par de grandes douleurs et souffrances. Mais le lac est moche, c'est le sourire du camion. Et je déteste les gens du diamètre de la vie de la communauté, mais le besoin est le besoin de l'environnement. Tortor aliquam no facilisi feugiat eu eu feugiat odium feugiat demain. Ou bien c'est un organisme organique qui n'a besoin de rien de facile. Il faut boire le plus possible. Le rire est un bon moyen de dessiner une couche du lac ou une solution de facilité. Euismod lacinia à quis risus sed vulputate. Convallis convallis tellus id parfois velit laoreet id. Car la maladie passe désormais par un Il aimait les deux ultricies du lac, mais elles étaient laides. Le portier de l'équipe de football attend le match avec impatience. Il est temps pour les enfants de prendre une salade et une salade. L'investissement en temps qu'aucun moteur diesel prévu n'a besoin d'être enceinte. Le football est présenté comme un lit de bière à boire. C'est pourquoi il veut raccrocher le dessin animé. Comment le lac pend parfois dans la gorge. L'auteur de Life promeut le football comme un lit de bière à boire. Eu feugiat pretium nibh ipsum conséquence.
Ullamcorper n’a besoin d’aucun soutien financier pour qui que ce soit. Ne vous inquiétez pas de la température de la levure ou de la porte clinique. Amet venenatis urne cursus eget maintenant scelerisque viverra mauris in. Ce devrait être une compagnie aérienne qui n'a pas besoin d'être malade. Qui se soucie des femmes enceintes ? Il est important d’être conscient de la situation actuelle de l’agent immobilier. Curabitur gravida arcu ac tortor dignissim convallis aenean et. Mais la haine du vulputaire flatte la vie des Mécènes. Qui est l'auteur d'Ultricies sinon mon vulputé ? Phasellus faucibus scelerisque eleifend jusqu'à pretium vulputate sapien. Le lit est une superbe urne fringilla porttitor rhoncus pain pure. Il n’y a pas de moment facile pour la maladie. Il est important d'être conscient de la situation. Il n’y a pas de camions pour Ultricies. Urna a maintenant besoin d'un dessin animé en chocolat pour mettre de la salade. Arcu cours vitae devoirs mauris rhoncus. Devoirs de vie Mauris Rhoncus Aenean ou Elit. Mais si la vie de la mère est enlevée à la mécène, diam. Car tout l’élément de l’oreiller n’est ni la vie ni la vie.
Duis at tellus à l'urne condimentum mattis pellentesque id nibh. Il n’est pas nécessaire d’utiliser des colorants, sauf si cela est très facile. Car la douleur pure n’est pas un élément présent. Il y avait aussi quelques flatteries. On dit que c’est une évidence. La masse du laid, mais l’élément temps, mais le prix du rire. Ou quel élément de l'oreiller n'est même pas ce que la piscine. Et le laid n'a besoin que de temps. Heureusement, il n’existe pas de moyen simple d’utiliser un véhicule. Bienvenue jusqu'à la messe de sapien faucibus et molestie et feugiat. Je veux décorer le lit. S'il vivait dans la rue, on disait que tout le monde devait être propre avec des flèches.
Les enfants n'ont même pas de salade ni de four à micro-ondes pour ça. Je déteste décorer un arc comme une salade. Pour que les enfants soient dignes, l'urne a besoin d'un parcours. Internet est un formidable outil. Malesuada a besoin d'une femme enceinte avec son partenaire. Lobortis mattis un peu de saveur dans la pâte. Que ce soit une grande masse de vie tortor sauce lacinia qui ou Couche Viverra chez les joueurs sauf. L’élément du libre marché ne flatte pas non plus la masse des salariés à l’heure actuelle. J'ai un week-end libre, mais demain je décorerai l'arc de Dieu. Le misérable besoin est le prix d'un grand carquois de bronze et du lit du vestibule. Il est donc également important que les joueurs soient purs et doux.
Il est facile de détester la maladie, mais à qui peut profiter la haine du bronze ? Un frémissement, un frémissement, une masse, une masse d'ultrices. Tant qu'il n'y a pas besoin d'acouphènes. Il veut le chasser avec des flèches. L'élément football est facile, mais qui déteste la maladie. C'est un élément facile à utiliser. Que ce soit une bonne chose que les diam mecenas ultricies mi eget mauris. C'est pellentesque elit ullamcorper dignissim demain tincidunt lobortis. Le porteur du lac pleure le fardeau de lui faire porter le fardeau, comme toujours. Tincidunt présente sempre feugiat nibh sed. Le rire des ultricies ne remplace pas la tristesse. Risus dans le hendrerit gravida rutrum tout le monde ne tellus orci ac. Je déteste décorer l'arc pour qu'il n'y ait pas de frémissement au loin. Ou jusqu'à ce que vous mangiez et détestiez le temps des protéines cliniques. Il doit être enceinte de ses partenaires et accoucher. Ils ne sont pas non plus membres de l'Arcitus. Doux maintenant mais toujours.
Il n’y a pas de moment facile pour la maladie des deux couches. Mettez le pot dans le fermenteur et ne touchez pas le couvercle. Faim malveillante et pauvreté horrible. Internet est un formidable outil contre la douleur. C'était un bon investissement pour les étudiants. La haine de Volutpat est facile de se laisser surprendre par la masse de la vie. Urna maintenant ce cours, certains craignent Elifend. Il faut un diam dans l'arc du parcours d'Euismod, qui est le dessinateur. Car je suis libre, mais je ne peux pas boire le mauvais goût de mon football. Car cela vaut la peine que l'urne empoisonnée ait maintenant besoin de chocolat. Et je déteste le moment du basket clinique dans les cibles maintenant. On dit qu’il n’y a pas d’investissement médical. Mais si la vie de la mère est enlevée à la mécène, diam. Diam maecenas ultricies mi eget mauris pharetra et ultrices neque. Et je déteste les enfants depuis longtemps, mais ils en ont besoin. Parfois, il est important de mettre Internet sur Internet. Passons maintenant à l'immobilier comme au terrain.
""".split(".")

# Pick random number of sentences to translate
num_lines = random.randint(0, len(lorem_sentences))
# Pick random starting point
starting = random.randint(0, len(lorem_sentences) - num_lines)

text_to_translate = '.'.join(lorem_sentences[starting:num_lines])

write_text(text_to_translate)


while True:
    continue

