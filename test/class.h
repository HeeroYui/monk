
namespace testMonk {
	class ClassNormal {
		public:
			ClassNormal();
			virtual ~ClassNormal();
	};
	class ClassHeritageSimple : public testMonk::ClassNormal {
		public:
			ClassHeritageSimple();
			virtual ~ClassHeritageSimple();
	};
	class ClassHeritageDouble : public testMonk::ClassNormal, public testMonk::ClassHeritageSimple {
		public:
			ClassHeritageDouble();
			virtual ~ClassHeritageDouble();
	};
	class ClassHeritagetemplate : public std::enable_shared_from_this<ClassHeritagetemplate> {
		public:
			ClassHeritagetemplate();
			virtual ~ClassHeritagetemplate();
	};
}
