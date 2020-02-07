using System;

namespace Uml.Cs.Dll
{
    public class UmlCsDll : ICanBeImplemented, IEquatable<UmlCsDll>
    {
        private string Str;

        protected UmlCsDll()
        {
        }

        public UmlCsDll(string str)
        {
            Str = str;
        }

        public bool HasString() => !string.IsNullOrEmpty(Str);

        public bool IsValid()
        {
            throw new NotImplementedException();
        }

        public bool Equals(UmlCsDll other)
        {
            throw new NotImplementedException();
        }
    }
}
