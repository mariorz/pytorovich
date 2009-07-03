


from distutils.core import setup 
import sys, os, os.path


setup(name = 'pytorovich',
      version = '0.1.1',
      description = 'Pytorovich is a PyGLPK wrapper for solving Linear Programming problems in a civilized manner. ',
      author = 'Mario Romero',
      author_email = 'mario@romero.fm',
      url = 'http://github.com/mariorz/pytorovich',
      license = 'GPL',
      classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Operating System :: Platform Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules' ],
      py_modules=['pytorovich']
)


